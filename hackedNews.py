"""
Sqlite: DB Connection
JSON: Json data
OS: use file paths on linux
urlli: needed by Auth0
logging: handle file logging
authlib: needed for OAuth
dotenv: used for env variables
flask: all necessary flask components
"""
import sqlite3
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from logging import FileHandler, WARNING
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, Response, request

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__, static_folder='static')
app.secret_key = env.get("APP_SECRET_KEY")
OAUTH = OAuth(app)

ADMIN_USERS = ["trevorfagan77@gmail.com", "joshlowe.cs@gmail.com", "chashimahiulislam@gmail.com"]

OAUTH.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

def get_db_connection():
    """
    This function returns a connection to the sqlite3 database
    """

    conn = sqlite3.connect('users.db', check_same_thread=False)
    return conn

@app.route('/remove_article', methods=["GET", "POST"])
def remove_article():
    """
    Endpoint for remove an article and querying database
    """
    data = request.form
    user_id = ""

    for key in data:
        user_id = key

    conn = get_db_connection()

    if session.get('user')['userinfo']['email'] in ADMIN_USERS:
        conn.execute('DELETE FROM LIKES WHERE article_id="' + user_id + '"')
    else:
        conn.execute('DELETE FROM Likes WHERE user_id="' + session.get('user')['userinfo']['sid'] \
        + '" AND article_id="' + user_id + '"')
    conn.commit()
    conn.close()

    return redirect('/likes')

@app.route('/add_like', methods=["GET", "POST"])
def add_like():
    """
    Endpoint for adding a like to an article and querying database
    """
    data = request.form
    return_data = []
    user_id = ""

    for key in data:
        user_id = key

    user_id = user_id[:-2]

    conn = get_db_connection()
    data = conn.execute("SELECT article_id, author, title, link FROM Articles WHERE article_id=" \
     + user_id).fetchall()
    conn.close()

    return_data.append(session.get('user')['userinfo']['sid'])

    for arr in data:
        for val in arr:
            return_data.append(val)

    conn = get_db_connection()
    if len(conn.execute('SELECT * FROM Likes WHERE user_id="' + return_data[0] + '" AND article_id="' + return_data[1] + '"').fetchall()) < 1:
        conn.execute('INSERT INTO Likes VALUES("' + str(return_data[0]) + '", "' + return_data[1] + '", "' + return_data[2] + '", "' + return_data[3] + '", "' + return_data[4] + '", True)')
        conn.commit()

    conn.close()

    return redirect('/')

@app.route('/add_dislike', methods=["GET", "POST"])
def add_dislike():
    """
    Endpoint for adding a dislike and querying database
    """
    data = request.form
    return_data = []
    user_id = ""

    for key in data:
        user_id = key

    user_id = user_id[:-2]

    conn = get_db_connection()
    data = conn.execute("""SELECT article_id, author, title, link FROM
     Articles WHERE article_id=""" + user_id).fetchall()
    conn.close()

    return_data.append(session.get('user')['userinfo']['sid'])

    for arr in data:
        for val in arr:
            return_data.append(val)

    conn = get_db_connection()
    if len(conn.execute('SELECT * FROM Likes WHERE user_id="' + return_data[0] + '" AND article_id="' + return_data[1] + '"').fetchall()) < 1:
        conn.execute('INSERT INTO Likes VALUES("' + str(return_data[0]) + '", "' + return_data[1] + '", "' + return_data[2] + '", "' + return_data[3] + '", "' + return_data[4] + '", False)')
        conn.commit()

    conn.close()

    return redirect('/')

@app.route('/', methods=["GET", "POST"])
def home():
    """
    This is the home route of our application.
    This page will show the list of articles from the hacker
    news API and give the user an option to log in.
    """

    conn = get_db_connection()
    data = conn.execute('SELECT * FROM Articles ORDER BY timestamp DESC').fetchall()
    conn.close()
    res = Response(render_template('index.html', data=data, session=session.get('user'), \
    pretty=json.dumps(session.get('user'), indent=4)))
    res.headers['X-Frame-Options'] = 'DENY'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.headers['X-XSS-Protection'] = 1
    res.headers['Strict-Transport-Security'] = 'max-age=63072000'
    res.headers['Content-Security-Policy'] = """default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'"""

    return res

@app.route("/login")
def login():
    """
    The login page is a redirect route for Auth0 to handle users logging in
    """
    return OAUTH.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route('/account')
def account():
    """
    The account page displays the user email, picture, and name
    """
    res = Response(render_template('account.html', session=session.get('user'), \
     pretty=json.dumps(session.get('user'), indent=4)))
    res.headers['X-Frame-Options'] = 'DENY'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.headers['X-XSS-Protection'] = 1
    res.headers['Strict-Transport-Security'] = 'max-age=63072000'
    res.headers['Content-Security-Policy'] = "default-src 'none'; img-src * 'self' data: https:; script-src 'self'; style-src 'self'"
    return res

@app.route('/likes')
def likes():
    """
    The likes page is only available for certain email addresses that are "admins"
    The likes page shows everyones likes and dislikes and allows the admin to remove them
    """
    is_admin = False

    if session.get('user')['userinfo']['email'] in ADMIN_USERS:
        is_admin = True

    data = ""

    conn = get_db_connection()
    if session.get('user')['userinfo']['email'] in ADMIN_USERS:
        data = conn.execute('SELECT * FROM Likes').fetchall()
    else:
        data = conn.execute('SELECT * FROM Likes WHERE user_id="' +  \
        session.get('user')['userinfo']['sid'] + '"').fetchall()

    conn.close()
    res = Response(render_template('likes.html', is_admin=is_admin, data=data, \
     session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
    res.headers['X-Frame-Options'] = 'DENY'
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.headers['X-XSS-Protection'] = 1
    res.headers['Strict-Transport-Security'] = 'max-age=63072000'
    res.headers['Content-Security-Policy'] = "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'"
    return res

@app.route("/callback", methods=["GET", "POST"])
def callback():
    """
    The callback function is a redirect route for Auth0
    """
    token = OAUTH.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    """
    This is the Auth0 route for logging the user out
    """
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

if __name__ == '__main__':
    app.run(debug=True)

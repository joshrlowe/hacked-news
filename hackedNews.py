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

FILE_HANDLER = FileHandler('error_log.txt')
FILE_HANDLER.setLevel(WARNING)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__, static_folder='static')
app.secret_key = env.get("APP_SECRET_KEY")
app.logger.addHandler(FILE_HANDLER)
OAUTH = OAuth(app)

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

@app.route('/add_like', methods=["GET", "POST"])
def add_like():
    data = request.form
    return_data = []
    id = ""

    for key in data:
        id = key

    id = id[:-2]

    conn = get_db_connection()
    data = conn.execute("SELECT article_id, author, title, link FROM Articles WHERE article_id=" + id).fetchall()
    conn.close()

    return_data.append(session.get('user')['userinfo']['aud'])

    for arr in data:
        for val in arr:
            return_data.append(val)

    # user_id, article_id, author, title, link, liked
    conn = get_db_connection()
    if len(conn.execute('SELECT * FROM Likes WHERE user_id="' + return_data[0] + '" AND article_id="' + return_data[1] + '"').fetchall()) < 1:
        conn.execute('INSERT INTO Likes VALUES("' + str(return_data[0]) + '", "' + return_data[1] + '", "' + return_data[2] + '", "' + return_data[3] + '", "' + return_data[4] + '", True)')
        conn.commit()

    conn.close()

    return redirect('/')

@app.route('/add_dislike', methods=["GET", "POST"])
def add_dislike():
    return "Dislike"

@app.route('/', methods=["GET", "POST"])
def home():
    """
    This is the home route of our application.
    This page will show the list of articles from the hacker
    news API and give the user an option to log in.
    """

    conn = get_db_connection()
    conn.execute('INSERT INTO Articles VALUES("sd", "dsd", "ds", "ds", True, DATETIME())')
    data = conn.execute('SELECT * FROM Articles').fetchall()
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
    res = Response(render_template('account.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
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
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM Likes').fetchall()
    conn.close()
    res = Response(render_template('likes.html', data=data, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
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

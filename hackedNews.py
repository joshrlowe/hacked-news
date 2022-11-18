from flask import Flask, render_template, Response
import requests
import sqlite3
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from logging import FileHandler, WARNING

file_handler = FileHandler('error_log.txt')
file_handler.setLevel(WARNING)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__, static_folder='static')
app.secret_key = env.get("APP_SECRET_KEY")
app.logger.addHandler(file_handler)
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

def get_db_connection():
        conn = sqlite3.connect('users.db', check_same_thread=False)
        return conn

@app.route('/')
def home():
        conn = get_db_connection()
#        conn.execute('INSERT INTO Articles VALUES("sd", "dsd", "ds", "ds", True, DATETIME())')
        data = conn.execute('SELECT * FROM Articles').fetchall()
        conn.close()
        res = Response(render_template('index.html', data=data, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
        res.headers['X-Frame-Options'] = 'DENY'
        res.headers['X-Content-Type-Options'] = 'nosniff'
        res.headers['X-XSS-Protection'] = 1
        res.headers['Strict-Transport-Security'] = 'max-age=63072000'
        res.headers['Content-Security-Policy'] = "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'"

        return res

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route('/account')
def account():
        res = Response(render_template('account.html', data=data, session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4)))
        res.headers['X-Frame-Options'] = 'DENY'
        res.headers['X-Content-Type-Options'] = 'nosniff'
        res.headers['X-XSS-Protection'] = 1
        res.headers['Strict-Transport-Security'] = 'max-age=63072000'
        res.headers['Content-Security-Policy'] = "default-src 'none'; img-src * 'self' data: https:; script-src 'self'; style-src 'self'"
        return "account"

@app.route('/likes')
def likes():
        conn = get_db_connection()
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
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
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

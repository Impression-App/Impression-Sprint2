# server.py
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=no-member
# pylint: disable=wrong-import-position
# pylint: disable=broad-except

import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio

################################

# Configuration and Variables

SERVER_PREFIX = "\033[96m" + "[SERVER]" + "\033[0m" + " "

dotenv_path = join(dirname(__file__), "secret.env")
load_dotenv(dotenv_path)

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

database_uri = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.session.commit()

import imp_util
import tables
import users
import groups

clients = []
print(SERVER_PREFIX + "Server started successfully")

################################

#### USERS

#### Given info from a user login, creates new user
@app.route("/new_user", methods=["POST"])
def on_new_user():
    data = flask.request.json
    try:
        fields = ["email", "given_name", "family_name", "picture"]
        for field in fields:
            if field not in data:
                data[field] = ""
        imp_util.users.new_user(
            data["email"], data["given_name"], data["family_name"], data["picture"]
        )
        imp_util.qr.create_new_qr_code(data["email"])
        return {"success": True, "email": data["email"]}
    except Exception as err:
        print(err)
        return {"success": False}


#### Given info from a user input, changes info of user on database
@app.route("/edit_user", methods=["POST"])
def on_edit():
    data = flask.request.json
    return imp_util.users.edit_user(data)


#### Given an email, returns a dictionary with the data of the user with such an email
@app.route("/get_user", methods=["POST"])
def get_user():
    query_user_email = flask.request.json
    return imp_util.users.get_user(query_user_email["email"])

#### GROUPS

#### Makes new group given name and user email

@app.route("/new_group", methods=["POST"])
def new_group():
    data = flask.request.json
    imp_util.groups.new_group(
        data["group_name"], data["user_id"]
    )
    return {"success": True, "group name": data["group_name"]}

#### Given a group name, returns a dict with info on group
@app.route("/get_group", methods=["POST"])
def get_group():
    name = flask.request.json
    return imp_util.groups.get_group(name["group_name"])

#### CONNECTIONS

#### Given 2 user emails, adds them as a new connection
#### to the DB if such a connection does not already exist.
#### Returns -1 if such a connection already exists,
#### and 0 if the connection was added.
@app.route("/new_connection", methods=["POST"])
def on_new_connection():
    data = flask.request.json
    return imp_util.connections.on_new_connection(data)


#### Given 2 user emails,
#### remove the exisiting connection between them if it exists.
#### Returns -1 if such a connection does not exist,
#### and 0 if the connection existed and was deleted.
@app.route("/delete_connection", methods=["POST"])
def on_delete_connection():
    data = flask.request.json
    return imp_util.connections.on_delete_connection(data)


#### Given a user X's email, returns a list of users X has a connection with.
#### Specifically, it returns a list of dictionaries
#### where each dictionary is the data of a user X has a connection with.
#### Used to query for all connections involving a given user.
@app.route("/query_connections", methods=["POST"])
def on_query_connections():
    data = flask.request.json
    return {
        "success": True,
        "connections": imp_util.connections.on_query_connections(data),
    }


@app.route("/")
def index():
    return "Hello World"


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=False,
    )

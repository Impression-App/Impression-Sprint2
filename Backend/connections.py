# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=missing-module-docstring
# pylint: disable=unused-import
# pylint: disable=broad-except

import flask_sqlalchemy
from server import DB
import tables
import users
import sys

#### Given 2 user emails,
#### adds them as a new connection to the DB if such a connection does not already exist.
#### Returns -1 if such a connection already exists, and 0 if the connection was added.
def on_new_connection(data):
    if data["user1_email"] == data["user2_email"]:
        return {"success": False}
    try:
        for connection in (
            DB.session.query(tables.Connections)
            .filter(
                (tables.Connections.user1_email == data["user1_email"])
                & (tables.Connections.user2_email == data["user2_email"])
            )
            .all()
        ):
            return users.get_user(data["user2_email"])
        for connection in (
            DB.session.query(tables.Connections)
            .filter(
                (tables.Connections.user1_email == data["user2_email"])
                & (tables.Connections.user2_email == data["user1_email"])
            )
            .all()
        ):
            return users.get_user(data["user2_email"])
        DB.session.add(tables.Connections(data["user1_email"], data["user2_email"]))
        DB.session.commit()
        return users.get_user(data["user2_email"])
    except:
        print("Error: Could not make a new connection")
        return {"success": False}
    finally:
        DB.session.close()


#### Given 2 user emails,
#### remove the exisiting connection between them if it exists.
#### Returns -1 if such a connection does not exist,
#### and 0 if the connection existed and was deleted.
def on_delete_connection(data):
    try:
        for connection in (
            DB.session.query(tables.Connections)
            .filter(
                (tables.Connections.user1_email == data["user1_email"])
                & (tables.Connections.user2_email == data["user2_email"])
            )
            .all()
        ):
            DB.session.delete(connection)
            DB.session.commit()
            return {"success":True}
        for connection in (
            DB.session.query(tables.Connections)
            .filter(
                (tables.Connections.user1_email == data["user2_email"])
                & (tables.Connections.user2_email == data["user1_email"])
            )
            .all()
        ):
            DB.session.delete(connection)
            DB.session.commit()
            return {"success":True}
    except:
        print("Error: could not delete connection")
        return {"success": False}
    finally:
        DB.session.close()
    return {"success":False}


#### Given a user X's email, returns a list of users X has a connection with.
#### Specifically, it returns a list of dictionaries
#### where each dictionary is the data of a user X has a connection with.
#### Used to query for all connections involving a given user.
def on_query_connections(data):
    result = []
    response = []
    try:
        result = (
            DB.session.query(tables.Connections)
            .filter(
                (tables.Connections.user1_email == data["user_email"])
                | (tables.Connections.user2_email == data["user_email"])
            )
            .all()
        )
        for connection in result:
            if connection.user1_email == data["user_email"]:
                connected_user = users.get_user(connection.user2_email)
                if connected_user != None:
                    response.append(connected_user)
            elif connection.user2_email == data["user_email"]:
                connected_user = users.get_user(connection.user1_email)
                if connected_user != None:
                    response.append(connected_user)
        return response
    except Exception as err:
        print(err)
        return {"success": False}
    finally:
        DB.session.close()

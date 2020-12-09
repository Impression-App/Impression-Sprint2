# pylint: disable=missing-function-docstring
# pylint: disable=no-member
# pylint: disable=missing-module-docstring
# pylint: disable=unused-import

import flask_sqlalchemy
from server import DB
import tables
import sys


#### Given an email, returns a dictionary with the data of the user with such an email
def get_user(query_user_email):
    try:
        user = DB.session.query(tables.Users).filter_by(email=query_user_email).first()
        if not user:
            return {}
        response = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization": user.organization,
            "descr": user.descr,
            "user_type": user.user_type,
            "gen_link_1": user.gen_link_1,
            "gen_link_2": user.gen_link_2,
            "gen_link_3": user.gen_link_3,
            "image": user.image,
            "doc": user.doc,
        }
        return response
    except:
        print("Error: cannot retrieve user")
        return {"success": False}
    finally:
        DB.session.close()


def new_user(email, fname, lname, image):
    try:
        user = DB.session.query(tables.Users).filter_by(email=email).all()
        if not user:
            DB.session.add(
                tables.Users(
                    email,
                    fname,
                    lname,
                    None,
                    None,
                    "Student",
                    None,
                    None,
                    None,
                    image,
                    None,
                )
            )
            DB.session.commit()
    except:
        print("Error: could not add new user")
    finally:
        DB.session.close()


def edit_user(account):
    try:
        user = DB.session.query(tables.Users).filter_by(email=account["email"]).first()
        user.email = account["email"]
        user.first_name = account["first_name"]
        user.last_name = account["last_name"]
        user.organization = account["organization"]
        user.descr = account["descr"]
        user.user_type = account["user_type"]
        user.gen_link_1 = account["gen_link_1"]
        user.gen_link_2 = account["gen_link_2"]
        DB.session.commit()
        return {"success": True}
    except:
        print("Error: cannot edit user")
        return {"success": False}
    finally:
        DB.session.close()

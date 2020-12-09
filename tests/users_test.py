# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-import
# pylint: disable=no-self-use
# pylint: disable=wrong-import-position

import unittest
import unittest.mock as mock
import sys

import os
from os.path import join, dirname
from dotenv import load_dotenv
import flask
import flask_sqlalchemy
import flask_socketio

sys.path.insert(1, "/home/ec2-user/environment/project3/Impression/Backend")
sys.path.append("/home/ec2-user/environment/project3/Impression/Backend")

import imp_util
import users
import tables

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

KEY_EMAIL = "email"
KEY_FNAME = "fname"
KEY_LNAME = "lname"
KEY_IMAGE = "image"

dummyUser = tables.Users(
    "dummy@gmail.com",
    "John",
    "Smith",
    "Impression Co",
    "Description",
    "Type",
    "link1",
    "link2",
    "link3",
    "image",
    "doc",
)

#### unit test for getting a user
class GetUser(unittest.TestCase):
    
    def mocked_query_2(self):
        return 5
    
    def mocked_user_query_first(self, email):
        mocked_user = mock.Mock()
        mocked_user.first.return_value = dummyUser
        return mocked_user

    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "dummy@gmail.com",
                KEY_EXPECTED: {
                    "email": "dummy@gmail.com",
                    "first_name": "John",
                    "last_name": "Smith",
                    "organization": "Impression Co",
                    "descr": "Description",
                    "user_type": "Type",
                    "gen_link_1": "link1",
                    "gen_link_2": "link2",
                    "gen_link_3": "link3",
                    "image": "image",
                    "doc": "doc",
                },
            },
        ]
        
        self.success_test_params_2 = [
            {
                KEY_INPUT: "dummy@gmail.com",
                KEY_EXPECTED: {"success": False},
            }
        ]

    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                "sqlalchemy.orm.query.Query.filter_by", self.mocked_user_query_first
            ):
                response = imp_util.users.get_user(test[KEY_INPUT])

                expected = test[KEY_EXPECTED]

            self.assertDictEqual(response, expected)
            
        for test in self.success_test_params_2:
            with mock.patch('sqlalchemy.orm.Query.first', self.mocked_query_2):
                response = imp_util.users.get_user(test[KEY_INPUT])

                expected = test[KEY_EXPECTED]

            self.assertDictEqual(response, expected)


#### unit test for editing a user
class EditUser(unittest.TestCase):


    def mocked_query_1(self):
        return dummyUser
    
    def mocked_user_query_first(self, email):
        mocked_user = mock.Mock()
        mocked_user.first.return_value = dummyUser
        return mocked_user

    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "",
                KEY_EXPECTED: "No errors",
            },
        ]
        
        self.edit_user_test_params = [
            {
                KEY_INPUT: {
                    "email": "dummy@gmail.com",
                    "first_name": "John",
                    "last_name": "Smith",
                    "organization": "Impression Co",
                    "descr": "Description",
                    "user_type": "Type",
                    "gen_link_1": "link1",
                    "gen_link_2": "link2",
                    "gen_link_3": "link3",
                    "image": "image",
                    "doc": "doc",
                },
                
                KEY_EXPECTED: {"success": True},
            },
        ]

    def test_get_user_success(self):
        for test in self.success_test_params:
            try:
                with mock.patch('sqlalchemy.orm.query.Query.filter_by',
                        self.mocked_user_query_first):
                    testing = imp_util.users.edit_user(test[KEY_INPUT])
                    response = "No errors"
            except AttributeError:
                response = "AttributeError"

            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
    
    def test_edit_user(self):
        for test in self.edit_user_test_params:
            try:
                with mock.patch('sqlalchemy.orm.Query.first', self.mocked_query_1):
                    response = imp_util.users.edit_user(test[KEY_INPUT])
            except AttributeError:
                response = "AttributeError"

            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)

#### unit test for making a new user
class NewUser(unittest.TestCase):
    def empty1(self, value):
        pass

    def mocked_user_query_all(self, email):
        mocked_user = mock.Mock()
        mocked_user.all.return_value = dummyUser
        return mocked_user

    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    KEY_EMAIL: "something@njit.edu",
                    KEY_FNAME: "Jane",
                    KEY_LNAME: "Doe",
                    KEY_IMAGE: "someimg",
                },
                KEY_EXPECTED: "No errors",
            },
        ]

    def test_get_user_success(self):
        for test in self.success_test_params:
            try:
                with mock.patch(
                    "sqlalchemy.orm.query.Query.filter_by", self.mocked_user_query_all
                ):
                    with mock.patch("sqlalchemy.orm.session.Session.add", self.empty1):
                        testing = imp_util.users.new_user(
                            test[KEY_INPUT][KEY_EMAIL],
                            test[KEY_INPUT][KEY_FNAME],
                            test[KEY_INPUT][KEY_LNAME],
                            test[KEY_INPUT][KEY_IMAGE],
                        )
                        response = "No errors"
            except AttributeError:
                response = "AttributeError"

            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)


if __name__ == "__main__":
    unittest.main()

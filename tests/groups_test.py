# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-import
# pylint: disable=no-self-use
# pylint: disable=wrong-import-position

import unittest
import unittest.mock as mock
import sys

sys.path.insert(1, "/home/ec2-user/environment/project3/Impression/Backend")
sys.path.append("/home/ec2-user/environment/project3/Impression/Backend")

import imp_util
import groups
import tables

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

KEY_GROUPID = "0"
KEY_EMAIL = "email"
KEY_GROUPNAME = "name"

dummyGroup = tables.Groups(
    "1",
    "dummy@gmail.com",
    "psuedogroup",
)


#### GET groups test
class GetGroups(unittest.TestCase):
    def mocked_group_query_all(self, email):
        mocked_group = mock.Mock()
        mocked_group.all.return_value = dummyGroup
        return mocked_group


    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "dummy@gmail.com",
                KEY_EXPECTED: {"success": False,},
            },
            # {
            #     KEY_INPUT: "dummy123@gmail.com",
            #     KEY_EXPECTED: {
            #         "success": False, 
            #     },
            # },
            # {
            #     KEY_INPUT: "",
            #     KEY_EXPECTED: {
            #         "success": False
                    
            #     },
            # },
        ]


    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                "sqlalchemy.orm.query.Query.all", self.mocked_group_query_all
            ):
                response = imp_util.groups.get_groups(test[KEY_INPUT])

                expected = test[KEY_EXPECTED]

            self.assertDictEqual(response, expected)

#### GET USERS test
class GetUsers(unittest.TestCase):
    def mocked_group_query_all(self, name, email):
        mocked_group = mock.Mock()
        mocked_group.all.return_value = dummyGroup
        return mocked_group

    def mocked_row2dict(self):
        dct = {}
        dct["pseudogroup"] = "dummy@gmail.com"
        return dct

    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "pseudogroup",
                KEY_EXPECTED: {"success": False},
                # KEY_INPUT: "groupname",
                # KEY_EXPECTED: {
                #     "success": False, 
                # },
                # KEY_INPUT: "",
                # KEY_EXPECTED: {
                #     "success": False
                    
                # },
            },
        ]


    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                "sqlalchemy.orm.query.Query.all", self.mocked_group_query_all
            ):
                with mock.patch(
                    "groups.row2dict", self.mocked_row2dict
                ):
                    response = imp_util.groups.get_users(test[KEY_INPUT])
                    expected = test[KEY_EXPECTED]
                self.assertDictEqual(response, expected)

#### NEW GROUP test
class NewGroup(unittest.TestCase):
    def mocked_add(self):
        pass

    def mocked_desc(self):
        pass


    def mocked_group_query_first(self, name):
        mocked_user = mock.Mock()
        mocked_user.first.return_value = dummyGroup
        return mocked_user


    def mocked_group_query_all(self, name):
        mocked_user = mock.Mock()
        mocked_user.all.return_value = dummyGroup
        return mocked_user


    def setUp(self):
        self.success_test_params = [
            # {
            #     KEY_INPUT: {
            #         KEY_GROUPNAME: "pseudogroup",
            #         KEY_EMAIL: "dummy@gmail.com",
            #     },
            #     KEY_EXPECTED: {
            #         "success": False,
            #     },
            # },
            {
                KEY_INPUT: {
                    KEY_GROUPNAME: "groupname",
                    KEY_EMAIL: "dummy123@gmail.com",
                },
                KEY_EXPECTED: {
                    "success": False,
                },
            },
            # {
            #     # KEY_INPUT: {
            #     #     KEY_GROUPNAME:"",
            #     #     KEY_EMAIL: "",
            #     # },
            #     # KEY_EXPECTED: {
            #     #     "success": False
                    
            #     # },
            # },
        ]


    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                "sqlalchemy.orm.query.Query.filter_by", self.mocked_group_query_all
            ):
                with mock.patch(
                    'sqlalchemy.orm.Query.order_by', self.mocked_group_query_first
                ):
                    with mock.patch(
                        "sqlalchemy.sql.expression.desc", self.mocked_desc
                    ):
                        with mock.patch(
                            "sqlalchemy.orm.session.Session.add", self.mocked_add
                        ):
                            response = imp_util.groups.new_group(
                                test[KEY_INPUT][KEY_GROUPNAME],
                                test[KEY_INPUT][KEY_EMAIL],
                                )
                            expected = test[KEY_EXPECTED]
                        self.assertDictEqual(response, expected)

#### ADD USER test
class AddUser(unittest.TestCase):
    def mocked_add(self):
        pass

    def mocked_order_by(self):
        pass

    def mocked_desc(self):
        pass

    def mocked_group_query_first(self, g_id, email, name):
        mocked_user = mock.Mock()
        mocked_user.first.return_value = dummyGroup
        return mocked_user

    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    KEY_GROUPNAME: "pseudogroup",
                    KEY_EMAIL: "dummy1@gmail.com",
                },
                KEY_EXPECTED: {
                    "success": False,
                },
            },
            # {
            #     # KEY_INPUT: {
            #     #     KEY_GROUPNAME: "",
            #     #     KEY_EMAIL: "",
            #     # },
            #     # KEY_EXPECTED: {
            #     #     "success": False
                    
            #     # },
            # },
        ]


    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                'sqlalchemy.orm.query.Query.filter_by', self.mocked_group_query_first
            ):
                with mock.patch(
                    'sqlalchemy.orm.Query.order_by', self.mocked_order_by
                ):
                    with mock.patch(
                        "sqlalchemy.sql.expression.desc", self.mocked_desc
                    ):
                        with mock.patch(
                            "sqlalchemy.orm.session.Session.add", self.mocked_add
                        ):
                            response = imp_util.groups.add_user(
                                test[KEY_INPUT][KEY_GROUPNAME], 
                                test[KEY_INPUT][KEY_EMAIL],
                                )
                            expected = test[KEY_EXPECTED]
                        self.assertDictEqual(response, expected)

#### LEAVE GROUP test
class LeaveGroup(unittest.TestCase):
    def mocked_delete(self):
        pass


    def mocked_group_query_first(self, g_id, name, email):
        mocked_user = mock.Mock()
        mocked_user.first.return_value = dummyGroup
        return mocked_user


    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: {
                    KEY_GROUPID: "1",
                    KEY_GROUPNAME: "pseudogroup",
                    KEY_EMAIL: "dummy@gmail.com",
                },
                KEY_EXPECTED: {
                    "success": False,
                },
            },
            # {
            #     # KEY_INPUT: {
            #     #     KEY_GROUPID: "",
            #     #     KEY_GROUPNAME: "",
            #     #     KEY_EMAIL: "",
            #     # },
            #     # KEY_EXPECTED: {
            #     #     "success": False
            #     # },
            # },
        ]


    def test_get_user_success(self):
        for test in self.success_test_params:
            with mock.patch(
                'sqlalchemy.orm.query.Query.filter_by', self.mocked_group_query_first
            ):
                with mock.patch( 
                    'sqlalchemy.orm.session.Session.delete', self.mocked_delete
                ):
                    response = imp_util.groups.leave_group(
                        test[KEY_INPUT][KEY_GROUPID],
                        test[KEY_INPUT][KEY_GROUPNAME],
                        test[KEY_INPUT][KEY_EMAIL],
                        )
                    expected = test[KEY_EXPECTED]
                self.assertDictEqual(response, expected)


if __name__ == "__main__":
    unittest.main()
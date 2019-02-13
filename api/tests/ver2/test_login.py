from api.tests.test_base import TestBase
from api.ver2.utils.strings import status_202, v2_url_prefix, status_401
from api.strings import status_key, name_key, data_key, error_key, status_400
from api.ver2.utils.login_test_data import *


class TestLogin(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_login(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_credentials)
        data = res.get_json()

        self.assertEqual(data[status_key], status_202)
        self.assertEqual(data[data_key][0][name_key], user_with_correct_credentials[name_key])
        self.assertEqual(res.status_code, status_202)

    def test_login_wrong_mail_pass(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_incorrect_credentials)
        data = res.get_json()

        self.assertEqual(data[status_key], status_401)
        self.assertEqual(data[error_key], 'Your email or password is incorrect')
        self.assertEqual(res.status_code, status_401)

    def test_login_empty_mail_pass(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_missing_credentials)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Please enter your email')
        self.assertEqual(res.status_code, status_400)

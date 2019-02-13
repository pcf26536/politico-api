from os import error

from api.tests.test_base import TestBase
from api.ver2.utils.strings import status_202, v2_url_prefix, status_401, user_key, token_key
from api.strings import status_key, name_key, data_key, error_key, status_400
from api.ver2.utils.signup_test_data import *


class TestSignUp(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_signup(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data)
        data = res.get_json()

        self.assertEqual(data[status_key], status_202)
        self.assertEqual(data[data_key][0][user_key][lname], user_with_correct_signup_data[lname])
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_202)

    def test_signup_missing_fields(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_missing_signup_data)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'please enter your first name')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_name_format(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_name_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'invalid last name')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_email_format(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_mail_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'invalid email entered')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_password_length(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_pass_length)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'the password entered is too short')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_passport_format(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_passport_url)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'wrong passport url format')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_phone_number(self):
        """ Tests login success """
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_phone_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[data_key][0][error_key], 'wrong phone number format')
        self.assertEqual(data[data_key][0][token_key], 'JWT TOKEN')
        self.assertEqual(res.status_code, status_400)

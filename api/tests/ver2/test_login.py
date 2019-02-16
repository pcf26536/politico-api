from api.tests.ver1.test_base import TestBase
from api.ver2.utils.strings import token_key, user_key
from api.strings import status_key, data_key, error_key, status_400, status_404, status_200
from api.ver2.utils.login_test_data import *
from api.strings import ver_2_url_prefix


class TestLogin(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            ver_2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        )

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_login(self):
        """ Tests login success """
        res = self.client.post(
            ver_2_url_prefix + '/auth/login',
            json=user_with_correct_credentials
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertIn(token_key, data[data_key][0])
        self.assertEqual(data[data_key][0][user_key][email], user_with_correct_credentials[email])
        self.assertEqual(res.status_code, status_200)

    def test_login_wrong_mail(self):
        res = self.client.post(
            ver_2_url_prefix + '/auth/login',
            json=user_with_incorrect_mail
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], "user does not exits in the database")
        self.assertEqual(res.status_code, status_404)

    def test_login_wrong_pass(self):
        res = self.client.post(
            ver_2_url_prefix + '/auth/login',
            json=user_with_incorrect_password
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Incorrect password provided')
        self.assertEqual(res.status_code, status_400)

    def test_login_empty_mail(self):
        res = self.client.post(
            ver_2_url_prefix + '/auth/login',
            json=user_with_missing_mail
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "email field is required to login")
        self.assertEqual(res.status_code, status_400)

    def test_login_empty_pass(self):
        res = self.client.post(
            ver_2_url_prefix + '/auth/login',
            json=user_with_missing_pass
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "password field is required to login")
        self.assertEqual(res.status_code, status_400)

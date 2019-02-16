from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix, user_key, token_key, user_entity
from api.ver2.utils.validators import invalid_name
from api.ver2.utils.signup_test_data import *
from api.strings import status_201
from api.ver2.utils.strings import status_202
from api.strings import status_key, name_key, data_key, error_key, status_400
from api.ver2.utils.login_test_data import *
from api.strings import ver_2_url_prefix


class TestSignUp(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_signup(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        )
        data = res.get_json()

        self.assertEqual(data[data_key][0][user_key][lname], user_with_correct_signup_data[lname])
        self.assertEqual(data[status_key], status_201)
        self.assertIn(token_key, data[data_key][0])
        self.assertEqual(res.status_code, status_201)

    def test_signup_missing_fields(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_missing_signup_data
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "firstname field is required to create {}".format(user_entity))
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_name_format(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_name_format
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            invalid_name(user_with_wrong_name_format[lname], lname)['message']
        )
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_email_format(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_mail_format
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Invalid email")
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_password_length(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_pass_length
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Password must be at least 6 characters long")
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_passport_format(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_passport_url
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            'Bad {} format [{}] has no file extension.'.format(pspt, user_with_wrong_passport_url[pspt])
        )
        self.assertEqual(res.status_code, status_400)

    def test_signup_wrong_phone_number(self):
        res = self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_wrong_phone_format
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Enter a valid phone number")
        self.assertEqual(res.status_code, status_400)

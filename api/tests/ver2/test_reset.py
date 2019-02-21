from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix
from api.strings import status_key, data_key, error_key, status_400, status_404
from api.strings import ver_2_url_prefix, status_200
from api.tests.ver2.test_data.signup_test_data \
    import user_with_correct_signup_data
from api.tests.ver2.test_data.reset_test_data import *

class TestResetPassword(TestBase):
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

    def test_reset(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_correct_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(
            data[data_key][0][email], user_with_correct_email[email])
        self.assertEqual(
            data[data_key][0]['message'],
            'Check your email for password reset link')
        self.assertEqual(res.status_code, status_200)

    def test_reset_with_wrong_mail(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_unexisting_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(
            data[error_key],
            'No user is registered with that email')
        self.assertEqual(res.status_code, status_404)

    def test_reset_invalid_mail(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_invalid_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Please enter a valid email')
        self.assertEqual(res.status_code, status_400)

    def test_reset_no_mail(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_no_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            'No Input Received: Please input an email to reset you password')
        self.assertEqual(res.status_code, status_400)

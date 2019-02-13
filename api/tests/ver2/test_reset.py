from api.tests.test_base import TestBase
from api.ver2.utils.strings import status_205, v2_url_prefix
from api.strings import status_key, data_key, error_key, status_400, status_404
from api.ver2.utils.reset_test_data import *


class TestResetPassword(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_reset(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_correct_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_205)
        self.assertEqual(data[data_key][0][email], user_with_correct_email[email])
        self.assertEqual(res.status_code, status_205)

    def test_reset_with_wrong_mail(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_unexisting_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'The email provided does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_reset_invalid_mail(self):
        res = self.client.post(
            v2_url_prefix + '/auth/reset',
            json=user_with_invalid_email)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Please enter a valid email')
        self.assertEqual(res.status_code, status_400)

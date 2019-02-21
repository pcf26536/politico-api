from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix
from api.strings import status_key, data_key, error_key, status_404, status_400
from api.tests.ver2.test_data.register_test_data import *
from api.tests.ver2.test_data.office_test_data import correct_office
from api.tests.ver2.test_data.party_test_data import correct_party
from api.tests.ver2.test_data.signup_test_data\
    import user_with_correct_signup_data, \
    user_with_correct_signup_data_2
from api.strings import status_201


class TestRegister(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        ) # user

        self.client.post(
            v2_url_prefix + '/parties',
            json=correct_party, headers=self.admin_headers)
        self.client.post(
            v2_url_prefix + '/offices',
            json=correct_office, headers=self.admin_headers)

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_register(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(
            data[data_key][0][candidate_key],
            correct_candidate_infor[candidate_key])
        self.assertEqual(res.status_code, status_201)

    def test_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/register',
            json=candidate_id_unexisting_infor,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected User does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_party_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/register',
            json=party_id_unexisting_info,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected Party does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/100000/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected Office does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_candidate_is_registered(self):
        self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        res = self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Candidate is already registered')
        self.assertEqual(res.status_code, status_400)

    def test_candidates_same_party_and_office(self):
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data_2,
            headers=self.admin_headers
        )  # another user

        self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        res = self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor_2,
            headers=self.admin_headers
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            'Two candidates from the same Party cannot be vie for one office')
        self.assertEqual(res.status_code, status_400)

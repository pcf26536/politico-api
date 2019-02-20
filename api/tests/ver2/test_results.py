from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix, token_key, authorization_key
from api.strings import status_key, data_key, error_key, status_404, status_200
from api.ver1.offices.strings import office_key
from api.ver2.utils.test_data.office_test_data import correct_office
from api.ver2.utils.test_data.party_test_data import correct_party
from api.ver2.utils.test_data.signup_test_data import user_with_correct_signup_data
from api.ver2.utils.test_data.register_test_data import correct_candidate_infor
from api.ver2.utils.test_data.vote_test_data import correct_vote
from api.ver2.utils.test_data.login_test_data import user_with_correct_credentials


class TestResults(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        )  # user
        res = self.client.post(
            '/api/v2/auth/login',
            json=user_with_correct_credentials
        )
        self.user_access_token = res.get_json()[data_key][0][token_key]
        self.user_headers = {authorization_key: 'Bearer {}'.format(self.user_access_token)}

        self.client.post(v2_url_prefix + '/parties', json=correct_party, headers=self.admin_headers)
        self.client.post(v2_url_prefix + '/offices', json=correct_office, headers=self.admin_headers)
        self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )
        self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote, headers=self.user_headers
        )

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_get_result(self):
        """ Tests get results success """
        res = self.client.get(
            v2_url_prefix + '/office/1/result', headers=self.user_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(data[data_key][0][office_key], "Women Representative")
        self.assertEqual(res.status_code, status_200)

    def test_get_results_office_id_not_found(self):
        """ Tests invalid office id """
        res = self.client.get(
            v2_url_prefix + '/office/10000000/result', headers=self.user_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Voting for the specified office has not commenced yet!')
        self.assertEqual(res.status_code, status_404)

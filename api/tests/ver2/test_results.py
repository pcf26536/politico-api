from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix
from api.strings import status_key, data_key, error_key, status_404, status_200
from api.ver1.offices.strings import office_key
from api.ver2.utils.office_test_data import correct_office
from api.ver2.utils.party_test_data import correct_party
from api.ver2.utils.signup_test_data import user_with_correct_signup_data
from api.ver2.utils.register_test_data import correct_candidate_infor
from api.ver2.utils.vote_test_data import correct_vote


class TestResults(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        )  # user
        self.client.post(v2_url_prefix + '/parties', json=correct_party)
        self.client.post(v2_url_prefix + '/offices', json=correct_office)
        self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.headers
        )
        self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote
        )

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_get_result(self):
        """ Tests get results success """
        res = self.client.get(
            v2_url_prefix + '/office/1/result')
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(data[data_key][0][office_key], 1)
        self.assertEqual(res.status_code, status_200)

    def test_get_results_office_id_not_found(self):
        """ Tests invalid office id """
        res = self.client.get(
            v2_url_prefix + '/office/10000000/result')
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Voting for the specified office has not commenced yet!')
        self.assertEqual(res.status_code, status_404)

        # def test_get_results_not_voted(self):
        # res = self.client.get(
        #    v2_url_prefix + '/office/1/result')
        # data = res.get_json()

        # self.assertEqual(data[status_key], status_404)
        # self.assertEqual(data[error_key], 'The specified office has no results yet!')
        # self.assertEqual(res.status_code, status_404)

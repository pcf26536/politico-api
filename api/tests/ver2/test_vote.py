from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix, authorization_key, token_key
from api.strings import status_key, data_key, error_key, status_404
from api.tests.ver2.test_data.office_test_data import correct_office
from api.tests.ver2.test_data.party_test_data import correct_party
from api.tests.ver2.test_data.signup_test_data import\
    user_with_correct_signup_data
from api.tests.ver2.test_data.register_test_data import correct_candidate_infor
from api.strings import status_201, status_400
from api.tests.ver2.test_data.login_test_data import \
    user_with_correct_credentials
from api.tests.ver2.test_data.vote_test_data import *
from api.ver1.ballot.strings import createdBy_key


class TestVote(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        ) # user
        res = self.client.post(
            '/api/v2/auth/login',
            json=user_with_correct_credentials
        )
        self.user_access_token = res.get_json()[data_key][0][token_key]
        self.user_headers = {
            authorization_key: 'Bearer {}'.format(self.user_access_token)}

        self.client.post(
            v2_url_prefix + '/parties',
            json=correct_party,
            headers=self.admin_headers)
        self.client.post(
            v2_url_prefix + '/offices',
            json=correct_office,
            headers=self.admin_headers)
        self.client.post(
            v2_url_prefix + '/office/1/register',
            json=correct_candidate_infor,
            headers=self.admin_headers
        )

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_vote(self):
        """ Tests vote success """
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote, headers=self.user_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(
            data[data_key][0]['createdby'], correct_vote[createdBy_key])
        self.assertEqual(res.status_code, status_201)

    def test_vote_voted(self):
        """ Tests vote voted """
        self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote, headers=self.user_headers)
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote, headers=self.user_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key], 'User has already voted for specified office')
        self.assertEqual(res.status_code, status_400)

    def test_voter_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=voter_does_not_exist_vote, headers=self.admin_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected User does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_vote_candidate_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=candidate_does_not_exist_vote, headers=self.user_headers)
        data = res.get_json()
        print(data)
        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], "Selected Candidate does not exist")
        self.assertEqual(res.status_code, status_404)

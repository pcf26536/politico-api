from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import  v2_url_prefix
from api.strings import status_key, data_key, error_key, status_404
from api.ver2.utils.test_data.vote_test_data import *
from api.ver1.ballot.strings import createdBy_key
from api.ver2.utils.test_data.office_test_data import correct_office
from api.ver2.utils.test_data.party_test_data import correct_party
from api.ver2.utils.test_data.signup_test_data import user_with_correct_signup_data
from api.ver2.utils.test_data.register_test_data import correct_candidate_infor
from api.strings import status_201, status_409


class TestVote(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()
        self.client.post(
            v2_url_prefix + '/auth/signup',
            json=user_with_correct_signup_data
        ) # user
        self.client.post(v2_url_prefix + '/parties', json=correct_party, headers=self.admin_headers)
        self.client.post(v2_url_prefix + '/offices', json=correct_office, headers=self.admin_headers)
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
            json=correct_vote, headers=self.admin_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0]['createdby'], correct_vote[createdBy_key])
        self.assertEqual(res.status_code, status_201)

    def test_vote_voted(self):
        """ Tests vote voted """
        self.client.post(v2_url_prefix + '/votes/', json=correct_vote, headers=self.admin_headers)
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote, headers=self.admin_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_409)
        self.assertEqual(data[error_key], 'User has already voted for specified office')
        self.assertEqual(res.status_code, status_409)

    def test_vote_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=office_does_not_exist_vote, headers=self.admin_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected Office does not exist')
        self.assertEqual(res.status_code, status_404)

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
            json=candidate_does_not_exist_vote, headers=self.admin_headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], "Selected Candidate does not exist")
        self.assertEqual(res.status_code, status_404)

from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import status_202, v2_url_prefix, status_403
from api.strings import status_key, data_key, error_key, status_404
from api.ver2.utils.vote_test_data import *
from api.ver1.ballot.strings import createdBy_key


class TestVote(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_vote(self):
        """ Tests vote success """
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote)
        data = res.get_json()

        self.assertEqual(data[status_key], status_202)
        self.assertEqual(data[data_key][0][createdBy_key], correct_vote[createdBy_key])
        self.assertEqual(res.status_code, status_202)

    def test_vote_voted(self):
        """ Tests vote voted """
        self.client.post(v2_url_prefix + '/votes/', json=correct_vote) # teardown
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=correct_vote)
        data = res.get_json()

        self.assertEqual(data[status_key], status_403)
        self.assertEqual(data[error_key], 'not allowed to vote twice for the same office')
        self.assertEqual(res.status_code, status_403)

    def test_vote_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=office_does_not_exist_vote)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'office id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_voter_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=voter_does_not_exist_vote)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'user id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_vote_candidate_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/votes/',
            json=candidate_does_not_exist_vote)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'candidate id was not found')
        self.assertEqual(res.status_code, status_404)

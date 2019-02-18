from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix, text_key, status_415
from api.strings import status_key, data_key, error_key, status_400, status_201, status_404
from api.ver2.utils.petition_test_data import *
from api.ver2.utils.office_test_data import correct_office
from api.ver2.utils.party_test_data import correct_party
from api.ver2.utils.signup_test_data import user_with_correct_signup_data
from api.ver2.utils.register_test_data import correct_candidate_infor
from api.ver2.utils.vote_test_data import correct_vote


class TestPetition(TestBase):
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

    def test_create_petition(self):
        res = self.client.post(
            v2_url_prefix + '/petitions/',
            json=correct_petition
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][body_key], correct_petition[body_key])
        self.assertEqual(res.status_code, status_201)

    def test_create_petition_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/petitions/',
            json=petition_with_wrong_office_id)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected Office does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_create_petition_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/petitions/',
            json=petition_with_wrong_user_id)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'Selected User does not exist')
        self.assertEqual(res.status_code, status_404)

    def test_create_petition_no_evidence(self):
        res = self.client.post(
            v2_url_prefix + '/petitions/',
            json=petition_with_no_evidence
        )
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'evidence field is required to create Petition')
        self.assertEqual(res.status_code, status_400)

    def test_create_petition_wrong_evidence_format(self):
        res = self.client.post(
            v2_url_prefix + '/petitions/',
            json=petition_with_wrong_evidence_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "Only ['png', 'jpg', 'gif', 'pdf', 'mp4', '3gp', 'mkv', 'mp3'] types allowed")
        self.assertEqual(res.status_code, status_400)

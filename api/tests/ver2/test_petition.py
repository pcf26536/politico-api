from api.tests.ver2.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix, text_key, status_415
from api.strings import status_key, data_key, error_key, status_400, status_201, status_404
from api.ver2.utils.petition_test_data import *


class TestPetition(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_create_petition(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=correct_petition)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][text_key], correct_petition[text_key])
        self.assertEqual(res.status_code, status_201)

    def test_create_petition_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=petition_with_wrong_office_id)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'office id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_create_petition_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=petition_with_wrong_user_id)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'user id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_create_petition_wrong_body_format(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=petition_with_wrong_body_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'the text entered is invalid')
        self.assertEqual(res.status_code, status_400)

    def test_create_petition_no_evidence(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=petition_with_no_evidence)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'no evidence has been provided for the petition')
        self.assertEqual(res.status_code, status_400)

    def test_create_petition_wrong_evidence_format(self):
        res = self.client.post(
            v2_url_prefix + '/petitions_bp/',
            json=petition_with_wrong_evidence_format)
        data = res.get_json()

        self.assertEqual(data[status_key], status_415)
        self.assertEqual(data[error_key], 'Invalid evidence format')
        self.assertEqual(res.status_code, status_415)

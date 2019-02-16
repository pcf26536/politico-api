from api.tests.ver1.test_base import TestBase
from api.ver2.utils.strings import status_202, v2_url_prefix
from api.strings import status_key, data_key, error_key, status_404
from api.ver2.utils.register_test_data import *
from api.ver1.offices.strings import office_key


class TestRegister(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_register(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/candids',
            json=correct_candidate_infor)
        data = res.get_json()

        self.assertEqual(data[status_key], status_202)
        self.assertEqual(data[data_key][0][office_key], correct_candidate_infor[office_key])
        self.assertEqual(res.status_code, status_202)

    def test_user_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/candids',
            json=candidate_id_unexisting_infor)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'user id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_party_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/candids',
            json=party_id_unexisting_info)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'party id was not found')
        self.assertEqual(res.status_code, status_404)

    def test_office_not_found(self):
        res = self.client.post(
            v2_url_prefix + '/office/1/candids',
            json=office_id_unexisting_info)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], 'office id was not found')
        self.assertEqual(res.status_code, status_404)

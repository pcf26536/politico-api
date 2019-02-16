from api.tests.ver1.test_base import TestBase
from api.ver2.utils.strings import v2_url_prefix
from api.strings import status_key, data_key, error_key, status_404, status_200
from api.ver1.offices.strings import office_key


class TestResults(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

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
        self.assertEqual(data[error_key], 'The office id was not found')
        self.assertEqual(res.status_code, status_404)

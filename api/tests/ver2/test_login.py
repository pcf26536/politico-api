from api.tests.test_base import TestBase
from api.ver2.utils.strings import status_202, v2_url_prefix
from api.strings import *


class TestLogin(TestBase):
    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        # close the db connection

    def test_login(self):
        """ Tests login success """
        res = self.client.post(v2_url_prefix + '/auth/signup', json={})
        data = res.get_json()

        self.assertEqual(data[status_key], status_202)
        self.assertEqual(data[data_key][0][name_key], self.office[name_key])
        self.assertEqual(res.status_code, status_202)

from .test_base import TestBase
from api.ver1.offices.models import political_offices
from api.strings import *
from api.ver1.offices.strings import *
from api.tests.strings import *


class TestOffices(TestBase):
    """ Tests for all offices endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.office = {
            name_key: "Women Representative",
            type_key : fed_type
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        political_offices.clear()

    # tests for POST offices
    def test_add_office_ep(self):
        """ Tests add office success """
        res = self.client.post('/api/v1/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][name_key], self.office[name_key])
        self.assertEqual(res.status_code, status_201)

    def test_add_office_missing_fields(self):
        """ Tests when some political office fields are missing e.g office name """
        res = self.client.post('/api/v1/offices', json={type_key: leg_type})
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], name_required)
        self.assertEqual(res.status_code, status_400)

    def test_add_office_no_data(self):
        """ Tests when no data is provided for add office"""
        res = self.client.post('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], no_data)
        self.assertEqual(res.status_code, status_400)

    # tests for GET all offices
    def test_get_all_offices_ep(self):
        """ Tests get all offices """
        no_of_offices = len(political_offices)

        res = self.client.get('/api/v1/offices')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), no_of_offices)
        self.assertEqual(res.status_code, status_201)

    # tests for GET single office
    def test_get_specific_office_ep(self):
        """ Tests get specific office """
        res = self.client.get('/api/v1/offices/1')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(res.status_code, status_201)

    def test_get_specific_office_id_not_found(self):
        """ Tests request made with id that does not exist """
        res = self.client.get('/api/v1/offices/14')
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], office_id_str + not_found)
        self.assertEqual(res.status_code, status_404)
        
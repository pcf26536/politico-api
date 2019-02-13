from api.tests.test_base import TestBase
from api.ver1.offices.models import political_offices
from api.strings import *
from api.ver1.offices.strings import *
from api.ver2.utils.strings import v2_url_prefix


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
        res = self.client.post(v2_url_prefix + '/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][name_key], self.office[name_key])
        self.assertEqual(res.status_code, status_201)

    def test_add_office_int_name(self):
        """ Tests when integer is provided for name """

        self.office[name_key] = 22
        res = self.client.post(v2_url_prefix + '/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Integer types are not allowed for a name field')
        self.assertEqual(res.status_code, status_400)

    def test_add_office_short_name(self):
        """ Tests when short name is provided """

        self.office[name_key] = 'ab'
        res = self.client.post(v2_url_prefix + '/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'The office name provided is too short')
        self.assertEqual(res.status_code, status_400)

    def test_add_office_exists(self):
        """ Tests add office success """
        self.client.post(v2_url_prefix + '/offices', json=self.office)
        res = self.client.post(v2_url_prefix + '/offices', json=self.office)
        data = res.get_json()

        self.assertEqual(data[status_key], status_409)
        self.assertEqual(
            data[error_key],
            "Conflict: office with Women Representative as name already exists")
        self.assertEqual(res.status_code, status_409)

    def test_add_office_missing_fields(self):
        """ Tests when some political office fields are missing e.g office name """
        res = self.client.post(v2_url_prefix + '/offices', json={type_key: leg_type})
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "name field is required. NOTE: required fields ['name', 'type'] to create office")
        self.assertEqual(res.status_code, status_400)

    def test_add_office_missing_fields_value(self):
        """ Tests when some political office fields are missing e.g office name """
        res = self.client.post(v2_url_prefix + '/offices', json={type_key: leg_type, name_key: ""})
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Please provide ['name'] value(s) for the office")
        self.assertEqual(res.status_code, status_400)

    def test_wrong_office_type(self):
        """ Tests when some political office fields are missing e.g office name """
        res = self.client.post(v2_url_prefix + '/offices', json={type_key: "Office", name_key: "MCA"})
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "Incorrect value [Office], office types should be ['federal', 'legislative', 'state', 'local government']"
        )
        self.assertEqual(res.status_code, status_400)

    def test_add_office_no_data(self):
        """ Tests when no data is provided for add office"""
        res = self.client.post(v2_url_prefix + '/offices')
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "No data was provided, fields ['name', 'type'] required to create office"
        )
        self.assertEqual(res.status_code, status_400)

    # tests for GET all offices
    def test_get_all_offices_ep(self):
        """ Tests get all offices """
        no_of_offices = len(political_offices)

        res = self.client.get(v2_url_prefix + '/offices')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), no_of_offices)
        self.assertEqual(res.status_code, status_201)

    # tests for GET single office
    def test_get_office_ep(self):
        """ Tests get specific office """
        # add a office cause of teardown clearing list
        self.client.post(v2_url_prefix + '/offices', json=self.office)
        res = self.client.get(v2_url_prefix + '/offices/1')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(res.status_code, status_201)

    def test_get_office_id_not_found(self):
        """ Tests request made with id that does not exist """
        res = self.client.get(v2_url_prefix + '/offices/14')
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], office_id_str + not_found)
        self.assertEqual(res.status_code, status_404)
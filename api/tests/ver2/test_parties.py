from api.tests.ver2.test_base import TestBase
from api.ver1.parties.models import political_parties
from api.strings import *
from api.ver1.parties.strings import *
from api.ver2.utils.strings import v2_url_prefix


class TestParties(TestBase):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.ex_party = {
            name_key: "African National Congress",
            hqAddKey: "14588-0100, Mombasa",
            logoUrlKey: "anc.gif"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        political_parties.clear()

    # tests for POST parties
    def test_add_party_ep(self):
        """ Tests create party success """
        res = self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][hqAddKey], self.ex_party[hqAddKey])
        self.assertEqual(res.status_code, status_201)
        
    def test_add_office_short_name(self):
        """ Tests when short name is provided """

        self.ex_party[name_key] = 'ab'
        res = self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'The party name [ab] provided is invalid/wrong format')
        self.assertEqual(res.status_code, status_400)
        
    def test_add_office_int_name(self):
        """ Tests when integer is provided for name """

        self.ex_party[name_key] = 22
        res = self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], 'Integer types are not allowed for a name field')
        self.assertEqual(res.status_code, status_400)

    def test_add_party_exists_ep(self):
        """ Tests create party success """
        self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        res = self.client.post(v2_url_prefix + '/parties',
                               json={
                                   name_key: "Aparty",
                                   hqAddKey: "14588-0100, Mombasa",
                                   logoUrlKey: "122fd.png"}, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], 409)
        self.assertEqual(data[error_key], "Conflict: party with 14588-0100, Mombasa as hqAddress already exists")
        self.assertEqual(res.status_code, 409)

    def test_add_party_missing_fields(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post(
            v2_url_prefix + '/parties',
            json={hqAddKey: "14588-0100, Mombasa", logoUrlKey: "anc.gif"}, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "name field is required to create party"
        )
        self.assertEqual(res.status_code, status_400)

    def test_add_party_missing_fields_value(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post(v2_url_prefix + '/parties',
                               json={name_key: " ", hqAddKey: "14588-0100, Mombasa", logoUrlKey: "anc.gif"},
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "The party name [ ] provided is invalid/wrong format")
        self.assertEqual(res.status_code, status_400)

    def test_add_party_wrong_value_format(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post(v2_url_prefix + '/parties',
                               json={name_key: "Aparty", hqAddKey: "14588-0100, Mombasa", logoUrlKey: "122fd"},
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Bad image logo format [122fd] has no file extension.")
        self.assertEqual(res.status_code, status_400)

    def test_add_party_no_data(self):
        """ Tests when no data is provided for create party"""
        res = self.client.post(v2_url_prefix + '/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(
            data[error_key],
            "No data was provided, fields ['name', 'hqAddress', 'logoUrl'] required to create party")
        self.assertEqual(res.status_code, status_400)

    # tests for GET all parties
    def test_get_all_parties_ep(self):
        """ Tests get all parties """
        res = self.client.get(v2_url_prefix + '/parties', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        # self.assertEqual(len(data[data_key]), no_of_parties)
        self.assertEqual(res.status_code, status_200)

    # tests for GET single party
    def test_get_specific_party_ep(self):
        """ Tests get specific party """
        self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        res = self.client.get(v2_url_prefix + '/parties/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(res.status_code, status_200)

    def test_get_specific_party_id_not_found(self):
        """ Tests request made with id that does not exist """
        res = self.client.get(v2_url_prefix + '/parties/14', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_key + ' ' + not_found)
        self.assertEqual(res.status_code, status_404)

    # tests for DELETE party
    def test_delete_party_ep(self):
        """ Tests when DELETE reuest made to /parties/<int:id> """
        self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)

        res = self.client.delete(v2_url_prefix + '/parties/1', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(data[data_key][0]['message'], 'African National Congress deleted successfully')
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(res.status_code, status_200)

    def test_delete_party_id_not_found(self):
        """ Tests DELETE request with party id that does not exist """
        res = self.client.delete(v2_url_prefix + '/parties/100000', headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_key + ' ' + not_found)
        self.assertEqual(res.status_code, status_404)

    # tests for PATCH party
    def test_patch_party(self):
        """ Tests PATCH request made to /parties/<int:id> """
        self.client.post(v2_url_prefix + '/parties', json=self.ex_party, headers=self.headers)
        res = self.client.patch(
            v2_url_prefix + '/parties/1/name',
            json={name_key: 'Iskerebete'}, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(data[data_key][0][name_key], 'Iskerebete')
        self.assertEqual(res.status_code, status_200)

    def test_patch_party_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """
        res = self.client.patch(
            v2_url_prefix + '/parties/100000/name',
            json={name_key: 'CORD'}, headers=self.headers)
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_key + ' ' + not_found)
        self.assertEqual(res.status_code, status_404)

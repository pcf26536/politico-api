from .test_base import TestBase
from api.ver1.parties.models import political_parties
from api.strings import *
from api.ver1.parties.strings import *
from api.tests.strings import *


class TestParties(TestBase):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.ex_party = {
            name_key: "African National Congress",
            hqAddKey: "14588-0100, Shimo la Tewa",
            logoUrlKey: "anc.gif"
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        political_parties.clear()

    # tests for POST parties
    def test_add_party_ep(self):
        """ Tests add party success """
        res = self.client.post('/api/v1/parties', json=self.ex_party)
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(data[data_key][0][hqAddKey], self.ex_party[hqAddKey])
        self.assertEqual(res.status_code, status_201)

    def test_add_party_exits_ep(self):
        """ Tests add party success """
        self.client.post('/api/v1/parties', json=self.ex_party)
        res = self.client.post('/api/v1/parties', json={ name_key: "A party", hqAddKey: "14588-0100, Shimo la Tewa", logoUrlKey: "122fd.png" })
        data = res.get_json()

        self.assertEqual(data[status_key], 409)
        self.assertEqual(data[error_key], "Conflict: party with 14588-0100, Shimo la Tewa as hqAddress already exists")
        self.assertEqual(res.status_code, 409)

    def test_add_party_missing_fields(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post('/api/v1/parties', json={ hqAddKey: "14588-0100, Shimo la Tewa", logoUrlKey: "anc.gif" })
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "name field is required. NOTE: required fields ['name', 'hqAddress', 'logoUrl'] to create party")
        self.assertEqual(res.status_code, status_400)

    def test_add_party_missing_fields_value(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post('/api/v1/parties', json={ name_key: " ", hqAddKey: "14588-0100, Shimo la Tewa", logoUrlKey: "anc.gif" })
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "The party name [ ] provided is too short or has a wrong format")
        self.assertEqual(res.status_code, status_400)

    def test_add_party_wrong_value_format(self):
        """ Tests when some political party fields are missing e.g logo url """
        res = self.client.post('/api/v1/parties', json={ name_key: "A party", hqAddKey: "14588-0100, Shimo la Tewa", logoUrlKey: "122fd" })
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "Bad image logo format [122fd] has no file extension.")
        self.assertEqual(res.status_code, status_400)

    def test_add_party_no_data(self):
        """ Tests when no data is provided for add party"""
        res = self.client.post('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data[status_key], status_400)
        self.assertEqual(data[error_key], "No data was provided, fields ['name', 'hqAddress', 'logoUrl'] required to create party")
        self.assertEqual(res.status_code, status_400)

    # tests for GET all parties
    def test_get_all_parties_ep(self):
        """ Tests get all parties """
        no_of_parties = len(political_parties)

        res = self.client.get('/api/v1/parties')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), no_of_parties)
        self.assertEqual(res.status_code, status_201)

    # tests for GET single party
    def test_get_specific_party_ep(self):
        """ Tests get specific party """
        self.client.post('/api/v1/parties', json=self.ex_party)
        res = self.client.get('/api/v1/parties/1')
        data = res.get_json()

        self.assertEqual(data[status_key], status_201)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(res.status_code, status_201)

    def test_get_specific_party_id_not_found(self):
        """ Tests request made with id that does not exist """
        res = self.client.get('/api/v1/parties/14')
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_id_str + not_found)
        self.assertEqual(res.status_code, status_404)

    # tests for DELETE party
    def test_delete_party_ep(self):
        """ Tests when DELETE reuest made to /parties/<int:id> """
        self.client.post('/api/v1/parties', json=self.ex_party) # add a party cause of teardown clearing list
        res = self.client.post('/api/v1/parties', json=self.ex_party)

        res = self.client.delete('/api/v1/parties/1')
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(data[data_key][0][msg_key], 'African National Congress deleted successfully')
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(res.status_code, status_200)

    def test_delete_party_id_not_found(self):
        """ Tests DELETE request with party id that does not exist """
        res = self.client.delete('/api/v1/parties/14')
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_id_str + not_found)
        self.assertEqual(res.status_code, status_404)

    # tests for PATCH party
    def test_patch_party(self):
        """ Tests PATCH request made to /parties/<int:id> """
        self.client.post('/api/v1/parties', json=self.ex_party) # add a party cause of teardown clearing list
        res = self.client.patch('/api/v1/parties/1/name', json={name_key: 'Iskerebete'})
        data = res.get_json()

        self.assertEqual(data[status_key], status_200)
        self.assertEqual(len(data[data_key]), 1)
        self.assertEqual(data[data_key][0][id_key], 1)
        self.assertEqual(data[data_key][0][name_key], 'Iskerebete')
        self.assertEqual(res.status_code, status_200)

    def test_patch_party_id_not_found(self):
        """ Tests PATCH request made with id that does not exist """
        res = self.client.patch('/api/v1/parties/14/name', json={name_key: 'CORD'})
        data = res.get_json()

        self.assertEqual(data[status_key], status_404)
        self.assertEqual(data[error_key], party_id_str + not_found)
        self.assertEqual(res.status_code, status_404)
        
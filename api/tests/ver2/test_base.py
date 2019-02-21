import unittest
from api import create_app
from api.ver2.database.model import Database
from api.ver1.users.strings import email
from api.ver2.utils.strings import password_key, token_key, authorization_key
from api.strings import data_key


class TestBase(unittest.TestCase):
    """ This is the super class for all tests """

    def setUp(self):
        """ Setup the common stuff """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # login as a admin
        res = self.client.post('/api/v2/auth/login', json={
            email: 'w.gichuhi5@students.ku.ac.ke', password_key: 'kadanieet'})

        self.admin_access_token = res.get_json()[data_key][0][token_key]
        self.admin_headers = {
            authorization_key: 'Bearer {}'
                               ''.format(self.admin_access_token)}

    def tearDown(self):
        self.app = None
        # clear the database here
        db = Database('testing')
        db.connect()
        db.truncate()
        db.drop_db_tables()

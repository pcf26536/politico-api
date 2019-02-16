import unittest
from api.ver2.database.model import Database


class TestDatabase(unittest.TestCase):
    """ Test database """

    def setUp(self):
        """ set up tests """

        self.db = Database('development')
        self.db.create_db_tables()
        self.db.create_root_user()

    def test_connect_db(self):
        """ Test whether connection is established """

        db = Database('development')
        self.assertTrue(db.connect())

    def test_connect_test_db(self):
        """ Test whether connection is established on test db """

        db = Database('testing')
        self.assertTrue(db.connect())

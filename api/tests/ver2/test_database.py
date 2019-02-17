import unittest
from api.ver2.database.model import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database('development')
        self.db.connect()
        self.db.create_db_tables()
        self.db.create_root_user()

    def test_connect_db(self):
        db = Database('development')
        self.assertTrue(db.connect())

    def test_connect_test_db(self):
        db = Database('testing')
        self.assertTrue(db.connect())

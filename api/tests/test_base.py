import unittest
from api import create_app


class TestBase(unittest.TestCase):
    """Default super class for api ver 1 tests"""

    # setup testing
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.item_list = []

    # deconstructs test elements
    def tearDown(self):
        self.app = None
        self.item_list.clear()

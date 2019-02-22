import unittest
from api import create_app


class TestTestingConfig(unittest.TestCase):
    """ Test class for testing config """

    def setUp(self):
        self.app = create_app('testing')

    def test_app_is_testing(self):
        """ Test function for testing environment """
        self.assertEqual(self.app.config['DEBUG'], True)
        self.assertEqual(self.app.config['TESTING'], True)

    def tearDown(self):
        self.app = None


class TestDevelopmentConfig(unittest.TestCase):
    """ Test class for development config """

    def setUp(self):
        self.app = create_app('development')

    def test_app_is_development(self):
        """ Test function for development environment """
        self.assertEqual(self.app.config['DEBUG'], True)
        self.assertEqual(self.app.config['TESTING'], False)

    def tearDown(self):
        self.app = None


class TestProductionConfig(unittest.TestCase):
    """ Test class for production config """

    def setUp(self):
        self.app = create_app('production')

    def test_app_is_production(self):
        """ Test function for production environment """
        self.assertEqual(self.app.config['DEBUG'], False)
        self.assertEqual(self.app.config['TESTING'], False)

    def tearDown(self):
        self.app = None

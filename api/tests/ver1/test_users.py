from api.tests.test_base import TestBase
from api.ver1.users.models import users
from api.strings import *
from api.ver1.users.models import *


class TestUsers(TestBase):
    """ Tests for all parties endpoints """

    def setUp(self):
        """ setup objects required for these tests """
        super().setUp()

        self.user = {
            fname : 'Jeptha',
            lname : 'Malela',
            email: 'malelalela@andela.com',
            phone: '+254 712 345 278',
            pspt : 'passport2.jpg',
            admin: False
        }

    # clear all lists after tests
    def tearDown(self):
        super().tearDown()
        users.clear()

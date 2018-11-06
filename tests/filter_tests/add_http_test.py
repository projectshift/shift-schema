from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import AddHttp


@attr('filter', 'add-http')
class AddHttpTest(TestCase):
    """ Add HTTP filter test"""

    def test_create(self):
        """ Can create add http filter """
        filter = AddHttp()
        self.assertIsInstance(filter, AddHttp)

    def test_add_http_to_string(self):
        """ Adding http to string if not present"""
        value = 'google.com'
        filter = AddHttp()
        self.assertEquals('http://google.com', filter.filter(value))

    def test_dont_add_if_present(self):
        """ Skip adding http if already present"""
        value = 'http://google.com'
        filter = AddHttp()
        self.assertEquals('http://google.com', filter.filter(value))

        value = 'https://google.com'
        filter = AddHttp()
        self.assertEquals('https://google.com', filter.filter(value))








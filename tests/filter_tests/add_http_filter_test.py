from unittest import TestCase

from shiftschema.filters import AddHttp


class AddHttpFilterTest(TestCase):
    """ Add HTTP filter test"""

    def test_create(self):
        """ Can create add http filter """
        filter = AddHttp()
        self.assertIsInstance(filter, AddHttp)

    def test_pass_through_non_strings(self):
        """ AddHttp: Pass through non-string values (don't do anything) """
        filter = AddHttp()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

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








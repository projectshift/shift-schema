from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import Uppercase


@attr('filter', 'uppercase')
class UppercaseTest(TestCase):
    """ Uppercase filter test"""

    def test_create(self):
        """ Can create uppercase filter """
        filter = Uppercase()
        self.assertIsInstance(filter, Uppercase)

    def test_pass_through_non_strings(self):
        """ uppercase: Pass through non-string values (don't do anything) """
        filter = Uppercase()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

    def test_filtering(self):
        """ Filtering value to uppercase """
        value = 'Me Is Value'
        filter = Uppercase()
        self.assertEqual(value.upper(), filter.filter(value))






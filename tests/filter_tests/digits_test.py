from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.exceptions import UnsupportedValueType
from shiftvalidate.filters import Digits

@attr('filter', 'digits')
class DigitsTest(TestCase):
    """ String strip filter test"""

    def test_create(self):
        """ Can create digits filter """
        filter = Digits()
        self.assertIsInstance(filter, Digits)

    def test_raise_on_bad_value(self):
        """ Raise in filtering bad value """
        value = 123
        filter = Digits()

        with self.assertRaises(UnsupportedValueType):
            filter.filter(value)

    def test_can_filter_digits(self):
        """ Can filter out the digits """
        value = '123 some string with 456 digits 789'
        expected = '123456789'

        filter = Digits()
        result = filter.filter(value)
        self.assertEqual(expected, result)

    def test_empty_string_if_not_found(self):
        """ Return empty string if no digits found """
        value = 'me contains no digits'
        filter = Digits()
        self.assertEqual('', filter.filter(value))





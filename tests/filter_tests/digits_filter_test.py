from unittest import TestCase

from shiftschema.filters import Digits


class DigitsFilterTest(TestCase):
    """ String digits filter test"""

    def test_create(self):
        """ Can create digits filter """
        filter = Digits()
        self.assertIsInstance(filter, Digits)

    def test_pass_through_non_strings(self):
        """ Digits: Pass through non-string values (don't do anything) """
        filter = Digits()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

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

    def test_convert_to_integer(self):
        """ Converting digits result to integer """
        value = 'I was born in 1964'
        filter = Digits(to_int=True)
        self.assertEqual(1964, filter.filter(value))






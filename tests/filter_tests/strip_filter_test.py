from unittest import TestCase
from shiftschema.filters import Strip
from shiftschema.exceptions import InvalidOption


class StripFilterTest(TestCase):
    """ String strip filter test"""

    def test_create(self):
        """ Can create strip filter """
        filter = Strip()
        self.assertIsInstance(filter, Strip)

    def test_pass_through_non_strings(self):
        """ Strip: Pass through non-string values (don't do anything) """
        filter = Strip()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

    def test_raise_on_invalid_mode(self):
        """ Raise error on invalid mode value """
        with self.assertRaises(InvalidOption):
            Strip(mode='BAD!')

    def test_can_filter(self):
        """ Can do filtering """
        value = '   filter me   '
        expected = 'filter me'
        strip = Strip()
        self.assertEqual(expected, strip.filter(value))

    def test_filter_left(self):
        """ Can filter from left side """
        value = '   filter me   '
        expected = 'filter me   '
        strip = Strip('left')
        self.assertEqual(expected, strip.filter(value))

    def test_filter_right(self):
        """ Can filter from right side """
        value = '   filter me   '
        expected = '   filter me'
        strip = Strip('right')
        self.assertEqual(expected, strip.filter(value))

    def test_filter_specific_chars(self):
        """ Can strip specific characters """
        value = '..www..filter me..www..'
        expected = 'filter me'
        strip = Strip(chars='w.')
        self.assertEqual(expected, strip.filter(value))





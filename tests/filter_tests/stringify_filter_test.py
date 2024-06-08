from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import Stringify
from shiftschema.exceptions import InvalidOption


@attr('filter', 'stringify')
class StringifyTest(TestCase):
    """ String strip filter test"""

    def test_create(self):
        """ Can create stringify filter """
        filter = Stringify()
        self.assertIsInstance(filter, Stringify)

    def test_can_filter(self):
        """ Can do filtering """
        value = None
        expected = 'None'
        strip = Stringify()
        self.assertEqual(expected, strip.filter(value))

    def test_can_filter_none_to_empty(self):
        """ Filter and convert None to empty string  """
        value = None
        expected = ''
        strip = Stringify(none_to_empty=True)
        self.assertEqual(expected, strip.filter(value))

    def test_can_filter_false_to_empty(self):
        """ Filter and convert False to empty string  """
        value = False
        expected = ''
        strip = Stringify(false_to_empty=True)
        self.assertEqual(expected, strip.filter(value))






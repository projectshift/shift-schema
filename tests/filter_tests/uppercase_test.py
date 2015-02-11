from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import Uppercase

@attr('filter', 'uppercase')
class UppercaseTest(TestCase):
    """ Uppercase filter test"""

    def test_create(self):
        """ Can create digits filter """
        filter = Uppercase()
        self.assertIsInstance(filter, Uppercase)

    def test_implicitly_convert_to_string(self):
        """ Implicitly convert value to string """
        value = 123456
        filter = Uppercase()
        self.assertEqual('123456', filter.filter(value))

    def test_filtering(self):
        """ Filtering value to uppercase """
        value = 'Me Is Value'
        filter = Uppercase()
        self.assertEqual(value.upper(), filter.filter(value))






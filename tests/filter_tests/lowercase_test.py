from unittest import TestCase
from nose.plugins.attrib import attr

from shiftschema.filters import Lowercase


@attr('filter', 'lowercase')
class LowercaseTest(TestCase):
    """ Lowercase filter test"""

    def test_create(self):
        """ Can create digits filter """
        filter = Lowercase()
        self.assertIsInstance(filter, Lowercase)

    def test_implicitly_convert_to_string(self):
        """ Implicitly convert value to string """
        value = 123456
        filter = Lowercase()
        self.assertEqual('123456', filter.filter(value))

    def test_filtering(self):
        """ Filtering value to lowercase """
        value = 'Me Is Value'
        filter = Lowercase()
        self.assertEqual(value.lower(), filter.filter(value))






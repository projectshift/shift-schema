from unittest import TestCase
from shiftschema.filters import Lowercase


class LowercaseFilterTest(TestCase):
    """ Lowercase filter test"""

    def test_create(self):
        """ Can create digits filter """
        filter = Lowercase()
        self.assertIsInstance(filter, Lowercase)

    def test_pass_through_non_strings(self):
        """ Lowercase: Pass through non-string values (don't do anything) """
        filter = Lowercase()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

    def test_filtering(self):
        """ Filtering value to lowercase """
        value = 'Me Is Value'
        filter = Lowercase()
        self.assertEqual(value.lower(), filter.filter(value))






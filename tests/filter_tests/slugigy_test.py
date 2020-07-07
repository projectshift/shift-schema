from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import Slugify


@attr('filter', 'slugify')
class UppercaseTest(TestCase):
    """ Slugify filter test"""

    def test_create(self):
        """ Can create slugify filter """
        filter = Slugify()
        self.assertIsInstance(filter, Slugify)

    def test_implicitly_convert_to_string(self):
        """ Implicitly convert value to string """
        value = 123456
        filter = Slugify()
        self.assertEqual('123456', filter.filter(value))

    def test_filtering(self):
        """ Filtering value to uppercase """
        value = 'Me Is a Value'
        filter = Slugify()
        result = filter.filter(value)
        self.assertEquals('me-is-a-value', result)

    def test_filtering_with_non_defaults(self):
        """ Can pass non-default slugify filer options"""
        value = 'Me Is a Value'
        filter = Slugify(separator='_', stopwords=('a', 'the'))
        result = filter.filter(value)
        expected = 'me_is_value'
        self.assertEquals(expected, result)







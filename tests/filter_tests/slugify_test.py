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

    def test_pass_through_non_strings(self):
        """ Slugify: Pass through non-string values (don't do anything) """
        filter = Slugify()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

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







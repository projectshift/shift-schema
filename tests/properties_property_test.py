from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.properties import Property
from shiftvalidate.filters.strip import Strip

@attr('property')
class PropertyTests(TestCase):
    """
    Simple property tests
    This hold tests for single processor property
    """

    def test_create_property(self):
        """ Can create property """
        property = Property()
        self.assertIsInstance(property, Property)


    def test_adding_filter(self):
        """ Add filter to property """
        property = Property()





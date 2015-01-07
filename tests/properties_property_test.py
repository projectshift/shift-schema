from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.properties import Property
from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.validators import Length

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

        filter = Strip()
        property.add_filter(filter)
        self.assertTrue(filter in property.filters)


    def test_raise_on_adding_bad_filter(self):
        """ Raise if adding filter of bad type """
        property = Property()

        with self.assertRaises(InvalidFilter):
            property.add_filter(mock.Mock())


    def test_adding_validator(self):
        """ Add validator to property """
        property = Property()

        validator = Length(min=10)
        property.add_validator(validator)
        self.assertTrue(validator in property.validators)


    def test_raise_on_adding_bad_validator(self):
        """ Raise if adding validator of bad type """
        property = Property()
        with self.assertRaises(InvalidValidator):
            property.add_validator(mock.Mock())


    def test_added_filter_and_validators_are_not_shared(self):
        """ Added filters and validators are not shared """

        property1 = Property()
        property2 = Property()


        property1.add_filter(Strip())
        property1.add_validator(Length())

        self.assertTrue(len(property2.filters) == 0)
        self.assertTrue(len(property2.validators) == 0)

        property3 = Property()
        self.assertTrue(len(property3.filters) == 0)
        self.assertTrue(len(property3.validators) == 0)


    def test_filter_value(self):
        """ Filtering property value with attached filters """
        property = Property()
        property.add_filter(Strip(mode='both'))
        property.add_filter(Digits())

        value = '  Good luck in 2015 to you!'
        self.assertEqual('2015', property.filter_value(value))








from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.property import SimpleProperty
from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.validators import Length, Digits as DigitsValidator

@attr('property', 'simple')
class SimplePropertyTests(TestCase):

    def test_create_simple_property(self):
        """ Creating simple property """
        prop = SimpleProperty()
        self.assertIsInstance(prop, SimpleProperty)

    def test_adding_filter(self):
        """ Add filter to property """
        prop = SimpleProperty()
        filter = Strip()
        prop.add_filter(filter)
        self.assertTrue(filter in prop.filters)

    def test_raise_on_adding_bad_filter(self):
        """ Raise if adding filter of bad type """
        prop = SimpleProperty()
        with self.assertRaises(InvalidFilter):
            prop.add_filter(mock.Mock())

    def test_adding_validator(self):
        """ Add validator to property """
        prop = SimpleProperty()
        validator = Length(min=10)
        prop.add_validator(validator)
        self.assertTrue(validator in prop.validators)

    def test_raise_on_adding_bad_validator(self):
        """ Raise if adding validator of bad type """
        prop = SimpleProperty()
        with self.assertRaises(InvalidValidator):
            prop.add_validator(mock.Mock())

    def test_added_filter_and_validators_are_not_shared(self):
        """ Added filters and validators are not shared """
        property1 = SimpleProperty()
        property2 = SimpleProperty()
        property1.add_filter(Strip())
        property1.add_validator(Length())

        self.assertTrue(len(property2.filters) == 0)
        self.assertTrue(len(property2.validators) == 0)

        property3 = SimpleProperty()
        self.assertTrue(len(property3.filters) == 0)
        self.assertTrue(len(property3.validators) == 0)

    def test_filter_value(self):
        """ Filtering property value with attached filters """
        property = SimpleProperty()
        property.add_filter(Strip(mode='both'))
        property.add_filter(Digits())
        value = '  Good luck in 2024 to you and your robots!'
        self.assertEqual('2024', property.filter_value(value))

    def test_validate_value_and_pass(self):
        """ Validate simple property and pass """
        property = SimpleProperty()
        property.add_validator(Length(min=3))
        result = property.validate_value('me is longer than three')
        self.assertTrue(type(result) is list)
        self.assertTrue(len(result) == 0)

    def test_validate_property_and_fail(self):
        """ Validate simple property and fail (return errors) """
        property = SimpleProperty()
        property.add_validator(Length(min=30))
        property.add_validator(DigitsValidator())
        result = property.validate_value('shorter than thirty')
        self.assertTrue(len(result) == 2)
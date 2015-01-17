
from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.schema import Schema
from shiftvalidate.property import SimpleProperty, EntityProperty
from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.exceptions import InvalidSchemaType
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.validators import Length, Digits as DigitsValidator

from tests import helpers

@attr('property', 'simple')
class SimplePropertyTests(TestCase):

    def test_create_simple_property(self):
        """ Creating simple property """
        prop = SimpleProperty()
        self.assertIsInstance(prop, SimpleProperty)

    def test_access_simple_property_required_status(self):
        """ Access required status through property descriptors """
        prop = SimpleProperty()
        self.assertFalse(prop.required)
        prop.required = True
        self.assertTrue(prop.required)

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

    def test_validate_required_property(self):
        """ Validating required simple properties """
        prop = SimpleProperty()
        prop.required = True
        result = prop.validate_value()
        self.assertTrue(type(result) is list)
        self.assertEqual(1, len(result))


@attr('property', 'entity')
class EntityPropertyTests(TestCase):

    def test_create_entity_property(self):
        """ Creating entity property """
        prop = EntityProperty()
        self.assertIsInstance(prop, EntityProperty)

    def test_access_entity_property_required_status(self):
        """ Access required status through property descriptors """
        prop = EntityProperty()
        self.assertFalse(prop.required)
        prop.required = True
        self.assertTrue(prop.required)

    def test_accessing_schema(self):
        """ Accessing nested schema with property descriptors """
        schema = Schema()
        prop = EntityProperty()
        self.assertIsNone(prop.schema)
        prop.schema = schema
        self.assertEqual(schema, prop.schema)

    def test_type_check_schema(self):
        """ Raise error on setting invalid schema """
        prop = EntityProperty()
        with self.assertRaises(InvalidSchemaType):
            prop.schema = dict()

    def test_filtering_model(self):
        """ Filtering nested entity """
        model = helpers.Person(
            first_name='   Willy    ',
            last_name='   Wonka    ',
        )
        prop = EntityProperty()
        prop.schema = Schema(helpers.person_spec)
        prop.filter(model)
        self.assertEqual('Willy', model.first_name)
        self.assertEqual('Wonka', model.last_name)

    def test_validating_model(self):
        """ Validated nested entity """
        class Model: pass
        class Nested: pass
        nested = Nested()
        model = Model()
        model.nested = nested

        class NestedSchema(Schema): pass

        nested_schema = NestedSchema()
        nested_schema.add_state_validator(helpers.StateValidatorInvalid())

        schema = Schema()
        schema.add_entity('nested')
        schema.nested.schema = nested_schema

        prop = EntityProperty()
        prop.schema = schema
        result = prop.validate(model)
        self.assertFalse(result)
        self.assertEqual(1, len(result.errors['nested']['__state__']))

    def test_filter_and_validate(self):
        """ Process: filter and validate in single operation """
        nested = helpers.Person(
            first_name='   W    ',
            last_name='   W    ',
        )
        model = helpers.Person()
        model.nested = nested

        nested_schema = Schema(helpers.person_spec)
        schema = Schema()
        schema.add_entity('nested')
        schema.nested.schema = nested_schema
        result = schema.process(model)

        self.assertEqual('W', model.nested.first_name)
        self.assertEqual('W', model.nested.last_name)

        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors['nested'])
        self.assertTrue('last_name' in result.errors['nested'])

    def test_validate_required_entity(self):
        """ Validating required entity properties """
        prop = EntityProperty()
        prop.required = True
        prop.schema = Schema()
        result = prop.validate()
        self.assertTrue(type(result) is list)
        self.assertEqual(1, len(result))
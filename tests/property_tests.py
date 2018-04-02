
from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.schema import Schema
from shiftschema.result import Result
from shiftschema.property import SimpleProperty
from shiftschema.property import EntityProperty
from shiftschema.property import CollectionProperty
from shiftschema.exceptions import InvalidFilter
from shiftschema.exceptions import InvalidValidator
from shiftschema.exceptions import InvalidSchemaType
from shiftschema import filters
from shiftschema import validators

from tests import helpers


@attr('property', 'simple')
class SimplePropertyTests(TestCase):

    def test_create_simple_property(self):
        """ Creating simple property """
        prop = SimpleProperty()
        self.assertIsInstance(prop, SimpleProperty)

    def test_adding_filter(self):
        """ Add filter to property """
        prop = SimpleProperty()
        filter = filters.Strip()
        prop.add_filter(filter)
        self.assertIn(filter, prop.filters)

    def test_raise_on_adding_bad_filter(self):
        """ Raise if adding filter of bad type """
        prop = SimpleProperty()
        with self.assertRaises(InvalidFilter):
            prop.add_filter(mock.Mock())

    def test_adding_validator(self):
        """ Add validator to property """
        prop = SimpleProperty()
        validator = validators.Length(min=10)
        prop.add_validator(validator)
        self.assertIn(validator, prop.validators)

    def test_raise_on_adding_bad_validator(self):
        """ Raise if adding validator of bad type """
        prop = SimpleProperty()
        with self.assertRaises(InvalidValidator):
            prop.add_validator(mock.Mock())

    def test_added_filter_and_validators_are_not_shared(self):
        """ Added filters and validators are not shared """
        property1 = SimpleProperty()
        property2 = SimpleProperty()
        property1.add_filter(filters.Strip())
        property1.add_validator(validators.Length())

        self.assertTrue(len(property2.filters) == 0)
        self.assertTrue(len(property2.validators) == 0)

        property3 = SimpleProperty()
        self.assertTrue(len(property3.filters) == 0)
        self.assertTrue(len(property3.validators) == 0)

    def test_filter_value(self):
        """ Filtering property value with attached filters """
        prop = SimpleProperty()
        prop.add_filter(filters.Strip(mode='both'))
        prop.add_filter(filters.Digits())
        value = '  Good luck in 2024 to you and your robots!'
        self.assertEqual('2024', prop.filter(value))

    def test_validate_value_and_pass(self):
        """ Validate simple property and pass """
        prop = SimpleProperty()
        prop.add_validator(validators.Length(min=3))
        result = prop.validate('me is longer than three')
        self.assertTrue(type(result) is list)
        self.assertTrue(len(result) == 0)

    def test_validate_property_and_fail(self):
        """ Validate simple property and fail (return errors) """
        prop = SimpleProperty()
        prop.add_validator(validators.Length(min=30))
        prop.add_validator(validators.Digits())
        result = prop.validate('shorter than thirty')
        self.assertTrue(len(result) == 2)


@attr('property', 'entity')
class EntityPropertyTests(TestCase):

    def test_create_entity_property(self):
        """ Creating entity property """
        prop = EntityProperty()
        self.assertIsInstance(prop, EntityProperty)

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

    def test_filtering_entity_with_filter_directly(self):
        """ Using filter on entity property """
        model = dict(something='nested')
        prop = EntityProperty()
        prop.add_filter(helpers.EntityFilter())
        filtered = prop.filter(model)
        self.assertEquals([model], filtered)

    def test_filtering_entity_with_schema(self):
        """ Filtering nested entity with schema """
        model = helpers.Person(
            first_name='   Willy    ',
            last_name='   Wonka    ',
        )
        prop = EntityProperty()
        prop.schema = Schema(helpers.person_spec)
        prop.filter_with_schema(model)
        self.assertEqual('Willy', model.first_name)
        self.assertEqual('Wonka', model.last_name)

    def test_validate_nested_entity_with_validators_attached_directly(self):
        """ Validate nested entity with validators attached directly"""
        prop = EntityProperty()
        prop.add_validator(helpers.ValidatorInvalid())
        result = prop.validate('Something')
        self.assertTrue(type(result) is list)
        self.assertEquals(1, len(result))

    def test_required_nested_entity_via_validator_attached_directly(self):
        """ Require nested entity via validator attached directly """
        prop = EntityProperty()
        prop.add_validator(validators.Required())
        result = prop.validate(value=None)
        self.assertEquals(1, len(result))

    def test_validating_nested_entity_with_schema(self):
        """ Validated nested entity with schema"""
        prop = EntityProperty()
        prop.schema = Schema()
        prop.schema.add_state_validator(helpers.ValidatorInvalid())
        prop.schema.add_property('simple')
        prop.schema.simple.add_validator(helpers.ValidatorInvalid())
        result = prop.validate_with_schema(dict())

        self.assertIsInstance(result, Result)
        self.assertFalse(result)
        self.assertIn('__state__', result.errors)
        self.assertIn('simple', result.errors)

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
        self.assertTrue('first_name' in result.errors['nested']['schema'])
        self.assertTrue('last_name' in result.errors['nested']['schema'])


@attr('property', 'collection', 'list')
class CollectionPropertyTests(TestCase):

    def test_create_collection_property(self):
        """ Creating collection property """
        prop = CollectionProperty()
        self.assertIsInstance(prop, CollectionProperty)

    def test_filtering_a_collection(self):
        """ Filtering a collection """
        collection = [
            dict(value=1),
            dict(value=2),
            dict(value=3),
            dict(value=4),
        ]

        prop = CollectionProperty()
        prop.add_filter(helpers.CollectionFilter())
        filtered = prop.filter(collection)
        self.assertEquals(2, filtered[0]['value'])
        self.assertEquals(4, filtered[1]['value'])

    def test_validating_a_collection(self):
        """ Validating a collection"""
        prop = CollectionProperty()
        prop.add_validator(validators.NotEmpty())
        result = prop.validate([])
        self.assertTrue(type(result) is list)
        self.assertEquals(1, len(result))

    def test_filter_collection_items_with_schema(self):
        """ Filter collection items with schema"""
        prop = CollectionProperty()
        prop.schema = Schema()
        prop.schema.add_property('name').add_filter(filters.Strip())

        collection = [
            dict(name='    Kady   '),
            dict(name='    Jeff   '),
        ]

        prop.filter_with_schema(collection)
        self.assertEquals('Kady', collection[0]['name'])
        self.assertEquals('Jeff', collection[1]['name'])

    def test_validate_collection_items_with_schema(self):
        """ Validate collection items with schema """
        prop = CollectionProperty()
        prop.schema = Schema()
        prop.schema.add_property('last_name')
        prop.schema.last_name.add_validator(validators.Required())

        collection = [
            dict(name='Kady', last_name=None),
            dict(name='Geoff', last_name='Petersen'),
            dict(name='Geoff', last_name=None),
            dict(name='Aneesa', last_name='Reyna'),
        ]

        result = prop.validate_with_schema(collection)

        self.assertTrue(type(result) is list)
        self.assertFalse(result[0])
        self.assertTrue(result[1])
        self.assertFalse(result[2])
        self.assertTrue(result[3])










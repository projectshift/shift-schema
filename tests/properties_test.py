from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.properties import Property, Entity
from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.validators import Length
from shiftvalidate.schema import Schema

from tests import helpers


@attr('properties', 'property')
class PropertyTests(TestCase):
    """
    Simple property tests
    This hold tests for simple schema property
    """

    def test_create_simple_property(self):
        """ Can create simple property """
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

        value = '  Good luck in 2024 to you and your robots!'
        self.assertEqual('2024', property.filter_value(value))





@attr('properties', 'entity')
class EntityTests(TestCase):
    """
    Linked entity property tests
    This hold tests for linked entity schema property
    """

    def test_create_linked_entity_property(self):
        """ Can create linked entity property """
        entity = Entity()
        self.assertIsInstance(entity, Entity)


    def test_setting_schema(self):
        """ Attaching nested schema """
        schema = Schema()
        entity = Entity()
        entity.set_schema(schema)
        self.assertEqual(schema, entity.schema)

    def test_raise_when_setting_bad_schema(self):
        """ Raise when trying to set schema of bad type """
        entity = Entity()
        with self.assertRaises(TypeError):
            entity.set_schema(dict())

    def test_can_filter_entity(self):
        """ Filtering linked entity property """
        model = helpers.Person(
            first_name='   Willy    ',
            last_name='   Wonka    ',
        )

        entity = Entity()
        entity.set_schema(Schema(helpers.person_spec))
        entity.filter(model)

        # assert filtered
        self.assertEqual('Willy', model.first_name)
        self.assertEqual('Wonka', model.last_name)


    def test_can_validate_entity(self):
        """ Validated linked entity property """
        model = helpers.Person(
            first_name='   Something very-very long indeed    ',
            last_name='   Not Wonka this time    ',
            salutation='dr'
        )

        entity = Entity()
        entity.set_schema(Schema(helpers.person_spec))
        result = entity.validate(model)

        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors)
        self.assertTrue('last_name' in result.errors)
        self.assertTrue('salutation' in result.errors)


    def test_can_process_entity(self):
        """ Filtering and validating at the same time """
        model = helpers.Person(
            first_name='   Willy    ',
            last_name='   Wonka    ',
            salutation='dr',
            birth_year='Someone wrote me in 1964',
        )

        entity = Entity()
        entity.set_schema(Schema(helpers.person_spec))
        result = entity.process(model)

        # assert filtered
        self.assertEqual('Willy', model.first_name)
        self.assertEqual('Wonka', model.last_name)
        self.assertEqual(1964, model.birth_year)

        # assert validated
        self.assertFalse(result)
        self.assertTrue('salutation' in result.errors)









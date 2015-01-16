from unittest import TestCase
from nose.plugins.attrib import attr

from shiftvalidate.schema import Schema
from shiftvalidate.exceptions import PropertyExists, InvalidValidator
from tests.helpers import person_spec, Person, StateValidator

@attr('schema')
class ErrorTest(TestCase):

    def test_create_schema(self):
        """ Creating a schema """
        schema = Schema()
        self.assertIsInstance(schema, Schema)

    def test_can_check_property_existence(self):
        """ Checking property existence on schema """
        schema = Schema()
        schema.properties['simple_property'] = 'property processor object'
        schema.entities['entity_property'] = 'entity processor object'
        self.assertTrue(schema.has_property('simple_property'))
        self.assertTrue(schema.has_property('entity_property'))

    def test_add_state_validator(self):
        """ Adding entity state validator to schema """
        validator = StateValidator()
        schema = Schema()
        schema.add_state_validator(validator)
        self.assertTrue(validator in schema.state)

    def test_raise_on_adding_bad_state_validator(self):
        """ Raise when adding state validator of bad type to schema """
        schema = Schema()
        with self.assertRaises(InvalidValidator):
            schema.add_state_validator(dict())

    def test_add_simple_property(self):
        """ Adding simple property to schema """
        schema = Schema()
        schema.add_property('simple')
        self.assertTrue('simple' in schema.properties)

    def test_raise_on_adding_existing_simple_property(self):
        """ Raise on adding simple property with existing name to schema"""
        schema = Schema()
        schema.add_property('simple')
        with self.assertRaises(PropertyExists):
            schema.add_property('simple')

    def test_add_entity_property(self):
        """ Adding linked entity property to schema """
        schema = Schema()
        schema.add_entity('entity')
        self.assertTrue('entity' in schema.entities)

    def test_raise_on_adding_existing_entity_property(self):
        """ Raise on adding entity property with existing name to schema """
        schema = Schema()
        schema.add_entity('entity')
        with self.assertRaises(PropertyExists):
            schema.add_entity('entity')

    def test_model_getter_on_dict(self):
        """ Using model-getter for dictionary-models """
        model = dict(someproperty='some value')
        schema = Schema()
        self.assertEqual('some value', schema.get(model, 'someproperty'))

    def test_model_getter_method(self):
        """ Model getter calls getter on model if present """
        class Model:
            def get_someproperty(self):
                return 'SOME VALUE'

        model = Model()
        schema = Schema()
        self.assertEqual('SOME VALUE', schema.get(model, 'someproperty'))

    def test_model_getter_attribute(self):
        """ Model getter falls back to attribute fetch if no getter on model"""
        class Model:
            someproperty = 'some value'

        model = Model()
        schema = Schema()
        self.assertEqual('some value', schema.get(model, 'someproperty'))


    def test_model_setter_on_dict(self):
        """ Using model setter for dictionary-models"""
        model = dict()
        schema = Schema()
        schema.set(model, 'someproperty', 'SOME VALUE')
        self.assertEqual('SOME VALUE', model['someproperty'])

    def test_model_setter_method(self):
        """ Model setter uses setter on model if present """
        class Model:
            def set_somevalue(self, value):
                self.somevalue = value

        model = Model()
        schema = Schema()
        schema.set(model, 'someproperty', 'some value')
        self.assertEqual('some value', model.__dict__['someproperty'])

    def test_model_setter_attribute(self):
        """ Model setter fallback to attribute set if no setter on model """
        class Model:
            pass

        model = Model()
        schema = Schema()
        schema.set(model, 'someproperty', 'SOME VALUE')
        self.assertEqual('SOME VALUE', model.someproperty)






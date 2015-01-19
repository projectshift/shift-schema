from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.schema import Schema
from shiftschema.result import Result
from shiftschema.property import SimpleProperty, EntityProperty
from shiftschema.exceptions import PropertyExists, InvalidValidator
from shiftschema.translator import Translator
from tests import helpers

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

    def test_access_properties_through_overloading(self):
        """ Overload access to schema properties """
        schema = Schema()
        schema.add_property('first_name')
        schema.add_entity('spouse')
        self.assertIsInstance(schema.first_name, SimpleProperty)
        self.assertIsInstance(schema.spouse, EntityProperty)
        with self.assertRaises(AttributeError):
            self.assertIsInstance(schema.nothinghere, EntityProperty)

    def test_add_state_validator(self):
        """ Adding entity state validator to schema """
        validator = helpers.StateValidator()
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

    def test_create_from_spec(self):
        """ Creating schema from spec"""
        schema = Schema(spec=helpers.person_spec_aggregate)
        self.assertEqual(1, len(schema.state))

        # import pdb;pdb.set_trace()
        self.assertIsInstance(schema.first_name, SimpleProperty)
        self.assertEqual(1, len(schema.first_name.filters))
        self.assertEqual(1, len(schema.first_name.validators))
        self.assertTrue(schema.first_name.required)

        self.assertIsInstance(schema.last_name, SimpleProperty)
        self.assertEqual(1, len(schema.last_name.filters))
        self.assertEqual(1, len(schema.last_name.validators))
        self.assertTrue(schema.last_name.required)


    def test_create_by_subclassing(self):
        """ Creating schema in subclass """
        class MySchema(Schema):
            def schema(self):
                self.add_property('property')
                self.add_entity('entity')

        schema = MySchema()
        self.assertTrue(schema.has_property('property'))
        self.assertTrue(schema.has_property('entity'))

    def test_filter_entity(self):
        """ Filtering entity with schema """
        schema = Schema(helpers.person_spec)
        person = helpers.Person(
            first_name = '  Willy  ',
            last_name = '  Wonka  ',
            salutation = ' mr ',
            birth_year = 'I was born in 1964'
        )
        schema.filter(person)
        self.assertEqual('Willy', person.first_name)
        self.assertEqual('Wonka', person.last_name)
        self.assertEqual('mr', person.salutation)
        self.assertEqual(1964, person.birth_year)

    def test_validate_state(self):
        """ Validating entity state """
        model = helpers.Person()
        schema = Schema()
        schema.add_state_validator(helpers.StateValidatorInvalid())
        result = schema.validate(model)
        self.assertIsInstance(result, Result)
        self.assertFalse(result)

    def test_validate_simple_properties(self):
        """ Validating simple properties """
        schema = Schema(helpers.person_spec)
        person = helpers.Person(
            first_name='Some really really long name',
            last_name='And a really really long last name',
            salutation='BAD!',
        )
        result = schema.validate(person)
        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors)
        self.assertTrue('last_name' in result.errors)
        self.assertTrue('salutation' in result.errors)

    def test_require_simple_properties(self):
        """ Validate required simple properties """
        class Model:
            def __init__(self):
                self.property=None

        model = Model()
        schema = Schema()
        schema.add_property('property')
        schema.property.required=True
        schema.property.required_message='Property required!'
        result = schema.validate(model)
        self.assertFalse(result)
        self.assertTrue('property' in result.errors)
        self.assertEqual(
            schema.property.required_message,
            result.errors['property'][0].message
        )

    def test_validate_entity_property(self):
        """ Validated linked entity properties with nested schemas """
        model = helpers.Person()
        model.spouse = helpers.Person(first_name='W', last_name='X')

        schema = Schema()
        schema.add_entity('spouse')
        schema.spouse.schema = Schema(helpers.person_spec)
        result = schema.validate(model)

        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors['spouse'])
        self.assertTrue('last_name' in result.errors['spouse'])

    def test_require_linked_entities(self):
        """ Validate required linked entities"""
        class Model:
            def __init__(self):
                self.entity=None

        model = Model()
        schema = Schema()
        schema.add_entity('entity')
        schema.entity.schema=Schema()
        schema.entity.required=True
        schema.entity.required_message='Entity required!'
        result = schema.validate(model)

        self.assertFalse(result)
        self.assertTrue('entity' in result.errors)
        self.assertEqual(
            schema.entity.required_message,
            result.errors['entity'][0].message
        )

    def test_validate_and_filter(self):
        """ Process: validation and filtering as single operation"""
        person = helpers.Person(first_name='   W   ')
        person.spouse = helpers.Person(first_name='   X   ')
        schema = Schema(helpers.person_spec_aggregate)
        result = schema.process(person)

        self.assertEqual('W', person.first_name)
        self.assertEqual('X', person.spouse.first_name)

        self.assertTrue('first_name' in result.errors) # too short
        self.assertTrue('first_name' in result.errors['spouse'])

        self.assertTrue('last_name' in result.errors) # required
        self.assertTrue('last_name' in result.errors['spouse'])

    def test_results_injected_with_translations(self):
        """ Schema-generated results are injected with translation settings """
        schema = Schema()
        result = schema.validate(mock.Mock())
        self.assertEqual('en', result.locale)
        self.assertIsInstance(result.translator, Translator)

        Schema.locale='ru'
        Schema.translator.add_location('/tmp')

        schema = Schema()
        result = schema.validate(mock.Mock())
        self.assertEqual('ru', result.locale)
        self.assertIsInstance(result.translator, Translator)
        self.assertTrue('/tmp' in result.translator.dirs)

    @attr('fixme')
    def test_do_not_skip_entity_validation_if_no_nested_schema(self):
        """
        Do not require nested schema to validate  nested entity
        for being required.
        """
        schema = Schema()
        schema.add_property('name')
        schema.add_entity('spouse')
        schema.name.required=True
        schema.spouse.required=True
        schema.spouse.schema = Schema()


        class Model:
            def __init__(self):
                self.name=None
                self.spouse=None

        p = Model()
        res=schema.validate(p)
        self.assertTrue('spouse' in res.errors)







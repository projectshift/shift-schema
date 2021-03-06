from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.schema import Schema
from shiftschema.result import Result
from shiftschema.property import SimpleProperty
from shiftschema.property import EntityProperty
from shiftschema.property import CollectionProperty
from shiftschema.exceptions import PropertyExists, InvalidValidator
from shiftschema.translator import Translator
from shiftschema import validators
from shiftschema import filters
from tests import helpers
from pprint import pprint as pp


@attr('schema')
class SchemaTest(TestCase):

    def test_create_schema(self):
        """ Creating a schema """
        schema = Schema()
        self.assertIsInstance(schema, Schema)

    def test_can_check_property_existence(self):
        """ Checking property existence on schema """
        schema = Schema()
        schema.properties['simple_property'] = 'property processor'
        schema.entities['entity_property'] = 'entity processor'
        schema.collections['collection_property'] = 'collection processor'
        self.assertTrue(schema.has_property('simple_property'))
        self.assertTrue(schema.has_property('entity_property'))
        self.assertTrue(schema.has_property('collection_property'))

    def test_access_properties_through_overloading(self):
        """ Overload access to schema properties """
        schema = Schema()
        schema.add_property('first_name')
        schema.add_entity('spouse')
        schema.add_collection('addresses')
        self.assertIsInstance(schema.first_name, SimpleProperty)
        self.assertIsInstance(schema.spouse, EntityProperty)
        self.assertIsInstance(schema.addresses, CollectionProperty)
        with self.assertRaises(AttributeError):
            self.assertIsInstance(schema.nothinghere, EntityProperty)

    def test_add_state_validator(self):
        """ Adding entity state validator to schema """
        validator = helpers.ValidatorValid()
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
        self.assertIn('simple', schema.properties)

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
        self.assertIn('entity', schema.entities)

    def test_raise_on_adding_existing_entity_property(self):
        """ Raise on adding entity property with existing name to schema """
        schema = Schema()
        schema.add_entity('entity')
        with self.assertRaises(PropertyExists):
            schema.add_entity('entity')

    def test_add_collection_property(self):
        """ Adding collection property to schema"""
        schema = Schema()
        schema.add_collection('collection_prop')
        self.assertIn('collection_prop', schema.collections)

    def test_raise_on_adding_existing_collection_property(self):
        """ Raise on adding collection property with existing name to schema """
        schema = Schema()
        schema.add_collection('collection_prop')
        with self.assertRaises(PropertyExists):
            schema.add_collection('collection_prop')

    def test_model_getter_on_dict(self):
        """ Using model-getter for dictionary-models """
        model = dict(someproperty='some value')
        schema = Schema()
        self.assertEqual('some value', schema.get(model, 'someproperty'))

    def test_model_getter_on_dict_returns_none_for_missing_keys(self):
        """ BUGFIX: do not explode on fetching value for missing dict key """
        model = dict(someproperty='some value')
        schema = Schema()
        self.assertIsNone(schema.get(model, 'me-is-missing'))

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

    def test_create_by_subclassing(self):
        """ Creating schema in subclass """
        class MySchema(Schema):
            def schema(self):
                self.add_property('property')
                self.add_entity('entity')

        schema = MySchema()
        self.assertTrue(schema.has_property('property'))
        self.assertTrue(schema.has_property('entity'))

    def test_filter(self):
        """ Filtering with schema """
        schema = helpers.PersonSpec()
        person = helpers.Person(
            first_name='  Willy  ',
            last_name='  Wonka  ',
            salutation=' mr ',
            birth_year='I was born in 1964'
        )
        schema.filter(person)
        self.assertEqual('Willy', person.first_name)
        self.assertEqual('Wonka', person.last_name)
        self.assertEqual('mr', person.salutation)
        self.assertEqual(1964, person.birth_year)

    def test_skip_all_filters_if_value_is_none(self):
        """ Skip filtering if value is none """
        schema = helpers.PersonSpec()
        person = helpers.Person()
        schema.filter(person)
        self.assertIsNone(person.first_name)
        self.assertIsNone(person.last_name)

    def test_filtering_simple_properties_with_context(self):
        """ Filtering simple properties with context (default)"""
        custom_context = 'I AM CUSTOM CONTEXT'

        class TestFilter(filters.AbstractFilter):
            def filter(self, value, model=None, context=None):
                if context == custom_context:
                    return 'CUSTOM CONTEXT'
                else:
                    return 'NO CUSTOM CONTEXT'

        class TestSchema(Schema):
            def schema(self):
                self.add_property('prop')
                self.prop.add_filter(TestFilter())

        model = dict(prop='some value')
        schema = TestSchema()
        schema.filter(model, context=custom_context)
        self.assertEquals('CUSTOM CONTEXT', model['prop'])

    def test_validate_state(self):
        """ Validating entity state """
        model = helpers.Person()
        schema = Schema()
        schema.add_state_validator(helpers.ValidatorInvalid())
        result = schema.validate(model)
        self.assertIsInstance(result, Result)
        self.assertFalse(result)

    def test_validate_simple_properties(self):
        """ Validating simple properties """
        schema = helpers.PersonSpec()
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

    def test_require_simple_properties_via_required_validator(self):
        """ Validate simple properties required via validator"""
        from shiftschema.validators import Required
        schema = Schema()
        schema.add_property('property')
        schema.property.add_validator(Required())
        result = schema.validate(dict())
        self.assertFalse(result)

    def test_validate_entity_property(self):
        """ Validated linked entity properties with nested schemas """
        model = helpers.Person()
        model.spouse = helpers.Person(first_name='W', last_name='X')

        schema = Schema()
        schema.add_entity('spouse')
        schema.spouse.schema = helpers.PersonSpec()
        result = schema.validate(model)

        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors['spouse']['schema'])
        self.assertTrue('last_name' in result.errors['spouse']['schema'])

    def test_entity_props_can_have_both_direct_and_schema_errors(self):
        """REGRESSION: Both direct and schema errors at the same time """
        person = helpers.Person()
        person.spouse = helpers.Person()

        schema = helpers.PersonSpec()
        schema.add_entity('spouse')
        schema.spouse.add_validator(helpers.ValidatorInvalid())
        schema.spouse.schema = helpers.PersonSpec()
        schema.spouse.schema.salutation.add_validator(validators.Required())
        result = schema.validate(person)

        self.assertTrue(len(result.errors['spouse']['direct']))
        self.assertIn('salutation', result.errors['spouse']['schema'])

    def test_require_linked_entities_with_validator_attached_directly(self):
        """ Require linked entities with validator attached directly """
        class Person:
            def __init__(self):
                self.spouse = None

        schema = Schema()
        schema.add_entity('spouse').add_validator(validators.Required())
        result = schema.validate(Person())
        self.assertFalse(result)
        self.assertIn('spouse', result.get_messages())

    def test_can_filter_out_collections_directly(self):
        """ Filter out collection properties with filters attached directly """
        address1 = helpers.Address(
            address='  2 Hollin Croft  ',
            city='  Barnsley  ',
            country='  UK  ',
            postcode='  S75 3TF  ',
        )

        address2 = helpers.Address(
            address='Newspaper House, 40 Churchgate',
            city='  Bolton  ',
            country='  UK  ',
        )

        address3 = helpers.Address(
            address='  446 Meadow Drive  ',
            city='  Billings, MT  ',
            country='US',
            postcode='  59101  ',
        )

        person = helpers.Person(
            first_name='Matthew',
            last_name='Rankin',
            salutation='mr',
            email='matrankin@gmail.com',
            birth_year='1964',
        )

        person.addresses.append(address1)
        person.addresses.append(address2)
        person.addresses.append(address3)

        schema = helpers.PersonSpecAggregate()
        schema.filter(person)
        self.assertEquals(2, len(person.addresses))
        for address in person.addresses:
            if address.country == 'US':
                self.fail('US address was not filtered out')

    def test_filter_collection_items_with_schemas(self):
        """ Filtering collection items with schema """
        address1 = helpers.Address(
            address='  2 Hollin Croft  ',
            city='  Barnsley  ',
            country='  UK  ',
            postcode='  S75 3TF  ',
        )

        person = helpers.Person(
            first_name='Matthew',
            last_name='Rankin',
            salutation='mr',
            email='matrankin@gmail.com',
            birth_year='1964',
        )

        person.addresses.append(address1)

        schema = helpers.PersonSpecCollectionAggregate()
        schema.filter(person)
        self.assertEquals('2 Hollin Croft', person.addresses[0].address)
        self.assertEquals('Barnsley', person.addresses[0].city)
        self.assertEquals('UK', person.addresses[0].country)
        self.assertEquals('S75 3TF', person.addresses[0].postcode)

    def test_can_validate_collections_directly(self):
        """ Validating collection with validators attached directly """
        person = helpers.Person(
            first_name='Matthew',
            last_name='Rankin',
            salutation='mr',
            email='matrankin@gmail.com',
            birth_year='1964',
        )

        schema = helpers.PersonSpecCollectionAggregate()
        result = schema.validate(person)
        self.assertFalse(result)
        self.assertIn('addresses', result.errors)

    def test_validate_collection_items_with_schemas(self):
        """ Validating collection items with schema """

        # valid
        address1 = helpers.Address(
            address='  2 Hollin Croft  ',
            city='  Barnsley  ',
            country='  UK  ',
            postcode='  S75 3TF  ',
        )

        # postcode required
        address2 = helpers.Address(
            address='Newspaper House, 40 Churchgate',
            city='  Bolton  ',
            country='  UK  ',
        )

        # filtered out
        address3 = helpers.Address(
            address='  446 Meadow Drive  ',
            city='  Billings, MT  ',
            country='US',
            postcode='  59101  ',
        )

        # address required
        address4 = helpers.Address(
            city='  Barnsley  ',
            country='  UK  ',
            postcode='  S75 3TF  ',
        )

        person = helpers.Person(
            first_name='Matthew',
            last_name='Rankin',
            salutation='mr',
            email='matrankin@gmail.com',
            birth_year='1964',
        )
        #
        person.addresses.append(address1)
        person.addresses.append(address2)
        person.addresses.append(address3)
        person.addresses.append(address4)

        schema = helpers.PersonSpecCollectionAggregate()
        result = schema.validate(person)

        self.assertFalse(result)
        collection = result.errors['addresses']['collection']

        self.assertIsInstance(collection[1], Result)
        self.assertFalse(collection[1])
        self.assertIn('postcode', collection[1].errors)

        self.assertIsInstance(collection[3], Result)
        self.assertFalse(collection[3])
        self.assertIn('address', collection[3].errors)

    def test_skip_validating_collection_with_schema_if_collection_empty(self):
        """ Skip validating collection with schema if it's empty or None """
        person = helpers.Person(
            first_name='Matthew',
            last_name='Rankin',
            salutation='mr',
            email='matrankin@gmail.com',
            birth_year='1964',
        )

        person.addresses = None  # override default
        schema = helpers.PersonSpecCollectionAggregate()
        schema.addresses.validators = []  # skip required validator
        result = schema.validate(person)
        self.assertTrue(result)

    def test_validate_and_filter(self):
        """ Process: validation and filtering as single operation"""
        person = helpers.Person(first_name='   W   ')
        person.spouse = helpers.Person(first_name='   X   ')
        schema = helpers.PersonSpecAggregate()
        result = schema.process(person)

        self.assertEqual('W', person.first_name)
        self.assertEqual('X', person.spouse.first_name)

        self.assertTrue('first_name' in result.errors) # too short
        self.assertTrue('first_name' in result.errors['spouse']['schema'])

    def test_results_injected_with_translations(self):
        """ Schema-generated results are injected with translation settings """
        schema = Schema()
        result = schema.validate(mock.Mock())
        self.assertEqual('en', result.locale)
        self.assertIsInstance(result.translator, Translator)

        Schema.locale = 'ru'
        Schema.translator.add_location('/tmp')

        schema = Schema()
        result = schema.validate(mock.Mock())
        self.assertEqual('ru', result.locale)
        self.assertIsInstance(result.translator, Translator)
        self.assertTrue('/tmp' in result.translator.dirs)










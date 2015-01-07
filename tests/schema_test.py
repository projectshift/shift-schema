from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.schema import Schema
from shiftvalidate.properties import Property, Collection, Entity
from shiftvalidate.validators import AbstractValidator, Length, Choice
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.results import SimpleResult
from shiftvalidate.exceptions import PropertyExists


# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------

class StateValidator(AbstractValidator):
    def validate(self, value=None, context=None):
        return SimpleResult() # always valid

person_spec = {
    'state': [StateValidator()],
    'properties': {
        'first_name': [
            Strip(),
            Length(min=1, max=10)
        ],
        'last_name': [
            Strip(),
            Length(min=1, max=10)
        ],
        'salutation': [
            Strip(),
            Choice(['mr', 'ms'])
        ],
        'birth_year': [
            Strip(),
            Digits()
        ]
    }
}


class Person:
    """
    Person
    Represents as entity being tested
    """
    def __init__(
        self,
        first_name=None,
        last_name=None,
        email=None,
        salutation=None,
        birth_year=None
    ):
        self.id = 123
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.salutation = salutation
        self.birth_year = birth_year


# -----------------------------------------------------------------------------

@attr('schema')
class ProcessorTests(TestCase):
    """
    Entity processor tests
    This hold tests for entity processor. Since it is abstract we'll need to
    test it through a concrete implementation.
    """

    def test_create_schema(self):
        """ Create processor, define filters  and validators"""
        schema = Schema()
        self.assertIsInstance(schema, Schema)

    def test_check_existence(self):
        """ Can check existence of properties, entities and collection """
        schema = Schema()
        schema.add_property('property')
        schema.add_entity('entity')
        schema.add_collection('collection')

        self.assertTrue(schema.has_property('property'))
        self.assertTrue(schema.has_property('entity'))
        self.assertTrue(schema.has_property('collection'))
        self.assertFalse(schema.has_property('nonexistent'))


    def test_add_simple_property(self):
        """ Adding simple property to schema """
        schema = Schema()
        schema.add_property('first_name')
        self.assertEqual(1, len(schema.properties))
        self.assertIsInstance(schema.properties['first_name'], Property)

    def test_add_state_validator(self):
        """ Adding entity state validator to schema """
        schema = Schema()
        state_validator = StateValidator()
        schema.add_state_validator(state_validator)
        self.assertTrue(state_validator in schema.state)

    def test_raise_in_state_validator_is_invalid(self):
        """ Raise if state validator does not implement AbstractValidator """
        schema = Schema()
        with self.assertRaises(TypeError):
            schema.add_state_validator(dict())


    def test_add_collection_property(self):
        """ Adding collection property to schema """
        schema = Schema()
        schema.add_collection('friends')
        self.assertEqual(1, len(schema.collections))
        self.assertIsInstance(schema.collections['friends'], Collection)

    def test_add_linked_entity_property(self):
        """ Adding linked entity property """
        schema = Schema()
        schema.add_entity('spouse')
        self.assertEqual(1, len(schema.entities))
        self.assertIsInstance(schema.entities['spouse'], Entity)

    def test_raise_on_existing_when_adding_property(self):
        """ Raise on existing when adding property """
        schema = Schema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_property('exists')

    def test_raise_on_existing_when_adding_collection(self):
        """ Raise on existing when adding collection """
        schema = Schema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_collection('exists')

    def test_raise_on_existing_when_adding_entity(self):
        """ Raise on existing when adding entity """
        schema = Schema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_entity('exists')

    def test_access_properties_through_overloading(self):
        """ Accessing properties through the dot """
        schema = Schema()

        # property
        schema.add_property('first_name')
        self.assertIsInstance(schema.first_name, Property)

        # entity
        schema.add_entity('spouse')
        self.assertIsInstance(schema.spouse, Entity)

        # collection
        schema.add_collection('friends')
        self.assertIsInstance(schema.friends, Collection)


    def test_initialize_from_spec(self):
        """ Initializing schema from spec """

        schema = Schema(person_spec)

        # state
        self.assertEqual(1, len(schema.state))

        # first name
        self.assertIsInstance(schema.first_name, Property)
        self.assertEqual(1, len(schema.first_name.filters))
        self.assertEqual(1, len(schema.first_name.validators))

        # last name
        self.assertIsInstance(schema.last_name, Property)
        self.assertEqual(1, len(schema.last_name.filters))
        self.assertEqual(1, len(schema.last_name.validators))

        # salutation
        self.assertIsInstance(schema.salutation, Property)
        self.assertEqual(1, len(schema.salutation.filters))
        self.assertEqual(1, len(schema.salutation.validators))

        # birth year
        self.assertIsInstance(schema.birth_year, Property)
        self.assertEqual(2, len(schema.birth_year.filters))
        self.assertEqual(0, len(schema.birth_year.validators))


    def test_initialize_in_subclass(self):
        """ Initialize in subclass """

        class PersonSchema(Schema):
            def schema(self):

                # state
                self.add_state_validator(StateValidator())

                self.add_property('first_name')
                self.first_name.add_filter(Strip())
                self.first_name.add_validator(Length(min=1, max=10))

                self.add_property('salutation')
                self.salutation.add_filter(Strip())
                self.salutation.add_validator(Choice(['mr', 'ms']))

        schema = PersonSchema()

        # state
        self.assertEqual(1, len(schema.state))

        # first name
        self.assertIsInstance(schema.first_name, Property)
        self.assertEqual(1, len(schema.first_name.filters))
        self.assertEqual(1, len(schema.first_name.validators))

        # salutation
        self.assertIsInstance(schema.salutation, Property)
        self.assertEqual(1, len(schema.salutation.filters))
        self.assertEqual(1, len(schema.salutation.validators))




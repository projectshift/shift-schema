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
            Digits(to_int=True)
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

    def __repr__(self):
        r = '<Person first=[{}] last=[{}] email=[{}] salutation=[{}] year=[{}]>'
        return r.format(
            self.first_name,
            self.last_name,
            self.email,
            self.salutation,
            self.birth_year
        )


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


    def test_filtering_entity(self):
        """ Performing filtering on a model """

        schema = Schema(person_spec)
        person = Person(
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


    def test_use_accessors_when_filtering(self):
        """ Filtering uses accessors if present """

        schema = Schema(person_spec)
        person = Person(
            first_name = '  Willy  ',
            last_name = '  Wonka  ',
            salutation = ' mr ',
            birth_year = 'I was born in 1964'
        )

        def getter(self):
            return self.first_name.upper()
        def setter(self, value):
            self.last_name = value.upper()

        # use getter
        person.get_first_name = getter
        person.set_last_name = setter

        schema.filter(person)
        self.assertEqual('WILLY', person.first_name)
        self.assertEqual('WONKA', person.last_name)


    def test_validate_entity_properties(self):
        """ Validating entity properties """
        schema = Schema(person_spec)
        person = Person(
            first_name='Some really really long name',
            last_name='And a really really long last name',
            salutation='BAD!',
        )

        result = schema.validate(person)
        self.assertFalse(result)
        self.assertTrue('first_name' in result.errors)
        self.assertTrue('last_name' in result.errors)
        self.assertTrue('salutation' in result.errors)
        self.assertTrue('birth_year' not in result.errors)


    def test_validate_entity_state(self):
        """ Validating entity state """
        class StateValidator(AbstractValidator):
            def validate(self, value=None, context=None):
                return SimpleResult(['error 1', 'error2'])

        schema = Schema(person_spec)
        schema.add_state_validator(StateValidator())


        person = Person(first_name = 'Willy', last_name = 'Wonka')
        result = schema.validate(person)
        self.assertTrue('__state__' in result.errors)
        self.assertEqual(2, len(result.errors['__state__']))

    def test_validate_and_filter_in_one_go(self):
        """ Process entity: validate and filter at the same time"""
        person = Person(
            first_name= '   Willy   ',
            last_name='  Not Wonka this time, but a really long last name',
            email='w.wonka@dactory.co.uk',
            salutation='dr',
            birth_year=' I was born in Chicago 1941'
        )
        schema = Schema(person_spec)
        result = schema.process(person)

        # assert filtered
        self.assertEqual('Willy', person.first_name)
        self.assertEqual(1941, person.birth_year)

        # assert has validation errors
        self.assertFalse(result)
        self.assertTrue('last_name' in result.errors)
        self.assertTrue('salutation' in result.errors)



    def test_skip_none_value(self):
        """ Processing skips none values """
        schema = Schema()
        schema.add_property('first_name')
        schema.first_name.add_filter(Strip())
        schema.first_name.add_validator(Length(max=10))

        schema.add_property('last_name')
        schema.last_name.add_filter(Strip())
        schema.last_name.add_validator(Length(max=10))

        schema.add_property('email')
        schema.email.add_filter(Strip())
        schema.email.add_validator(Length(max=10))

        schema.add_property('salutation')
        schema.salutation.add_filter(Strip())
        schema.salutation.add_validator(Choice(['mr', 'ms']))

        schema.add_property('birth_year')
        schema.birth_year.add_filter(Strip())
        schema.birth_year.add_filter(Digits())

        person = Person()
        result = schema.validate(person)
        self.assertTrue(result)









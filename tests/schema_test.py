from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.schema import Schema
from shiftvalidate.properties import Property, Collection, Entity
from shiftvalidate.exceptions import PropertyExists


class Person:
    """
    Person
    Represents as entity being tested
    """
    def __init__(self, first_name=None, last_name=None, email=None):
        self.id = 123
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class PersonSchema(Schema):
    """
    Person processor
    Holds a collection of filters and validators for processing person
    entity
    """
    pass
    #spec = {}
    # spec = {
    #     'state': [
    #         StateValidator1(),
    #         StateValidator2(),
    #     ],
    #     'collections': {
    #         'friends': [
    #             CollectionProcessor1(),
    #             CollectionProcessor2(),
    #         ],
    #         'enemies': [
    #             CollectionProcessor1(),
    #             CollectionProcessor2(),
    #         ],
    #     },
    #
    #     'entities': {
    #         'spouse': [
    #             EntityProcessor1(),
    #             EntityProcessor2()
    #         ],
    #         'child': [
    #             EntityProcessor1(),
    #             EntityProcessor2()
    #         ]
    #     },
    #
    #     'id': [
    #         Integer(),
    #     ]
    # }


@attr('schema')
class ProcessorTests(TestCase):
    """
    Entity processor tests
    This hold tests for entity processor. Since it is abstract we'll need to
    test it through a concrete implementation.
    """

    def test_create_schema(self):
        """ Create processor, define filters  and validators"""
        schema = PersonSchema()
        self.assertIsInstance(schema, PersonSchema)

    def test_check_existence(self):
        """ Can check existence of properties, entities and collection """
        schema = PersonSchema()
        schema.add_property('property')
        schema.add_entity('entity')
        schema.add_collection('collection')

        self.assertTrue(schema.has_property('property'))
        self.assertTrue(schema.has_property('entity'))
        self.assertTrue(schema.has_property('collection'))
        self.assertFalse(schema.has_property('nonexistent'))


    def test_add_simple_property(self):
        """ Adding simple property to schema """
        schema = PersonSchema()
        schema.add_property('first_name')
        self.assertEqual(1, len(schema.properties))
        self.assertIsInstance(schema.properties['first_name'], Property)

    def test_add_collection_property(self):
        """ Adding collection property to schema """
        schema = PersonSchema()
        schema.add_collection('friends')
        self.assertEqual(1, len(schema.collections))
        self.assertIsInstance(schema.collections['friends'], Collection)

    def test_add_linked_entity_property(self):
        """ Adding linked entity property """
        schema = PersonSchema()
        schema.add_entity('spouse')
        self.assertEqual(1, len(schema.entities))
        self.assertIsInstance(schema.entities['spouse'], Entity)

    def test_raise_on_existing_when_adding_property(self):
        """ Raise on existing when adding property """
        schema = PersonSchema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_property('exists')

    def test_raise_on_existing_when_adding_collection(self):
        """ Raise on existing when adding collection """
        schema = PersonSchema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_collection('exists')

    def test_raise_on_existing_when_adding_entity(self):
        """ Raise on existing when adding entity """
        schema = PersonSchema()
        schema.add_property('exists')
        with self.assertRaises(PropertyExists):
            schema.add_entity('exists')

    def test_access_properties_through_overloading(self):
        """ Accessing properties through the dot """
        schema = PersonSchema()

        # property
        schema.add_property('first_name')
        self.assertIsInstance(schema.first_name, Property)

        # entity
        schema.add_entity('spouse')
        self.assertIsInstance(schema.spouse, Entity)

        # collection
        schema.add_collection('friends')
        self.assertIsInstance(schema.friends, Collection)

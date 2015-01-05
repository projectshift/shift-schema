from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.results import SimpleResult
from shiftvalidate.processor import Processor


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


class PersonProcessor(Processor):
    """
    Person processor
    Holds a collection of filters and validators for processing person
    entity
    """
    spec = {
        'state': [
            StateValidator1(),
            StateValidator2(),
        ],
        'collections': {
            'friends': [
                CollectionProcessor1(),
                CollectionProcessor2(),
            ],
            'enemies': [
                CollectionProcessor1(),
                CollectionProcessor2(),
            ],
        },

        'entities': {
            'spouse': [
                EntityProcessor1(),
                EntityProcessor2()
            ],
            'child': [
                EntityProcessor1(),
                EntityProcessor2()
            ]
        },

        'id': [
            Integer(),
        ]
    }


class ProcessorTests(TestCase):
    """
    Entity processor tests
    This hold tests for entity processor. Since it is abstract we'll need to
    test it through a concrete implementation.
    """

    def test_create_processor(self):
        """ Create processor, define filters  and validators"""
        processor = PersonProcessor()
        self.assertIsInstance(processor, PersonProcessor)


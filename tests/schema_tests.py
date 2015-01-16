from unittest import TestCase
from nose.plugins.attrib import attr

from shiftvalidate.schema import Schema

@attr('schema')
class ErrorTest(TestCase):

    def test_create_schema(self):
        """ Creating a schema """
        schema = Schema()
        self.assertIsInstance(schema, Schema)

from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.validators import AbstractValidator
from shiftvalidate.exceptions import InvalidErrorType


@attr('validator', 'abstract')
class AbstractTest(TestCase):
    """ Abstract validator tests"""

    def test_can_extend(self):
        """ Can extend from abstract """
        class Custom(AbstractValidator):
            def validate(self, value, context=None):
                return 'Error'

        validator = Custom()
        self.assertIsInstance(validator, AbstractValidator)

    def test_raise_on_bad_validation_result(self):
        """ Raise if validator returns bad type of result """
        class Custom(AbstractValidator):
            def validate(self, value, context=None):
                return 'Error'

        with self.assertRaises(InvalidErrorType):
            validator = Custom()
            validator.run('some value')



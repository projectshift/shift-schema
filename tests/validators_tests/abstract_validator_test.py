from unittest import TestCase
from shiftschema.validators import AbstractValidator
from shiftschema.exceptions import InvalidErrorType


class AbstractValidatorTest(TestCase):
    """ Abstract validator tests"""

    def test_can_extend(self):
        """ Can extend from abstract """
        class Custom(AbstractValidator):
            def validate(self, value, model=None, context=None):
                return 'Error'

        validator = Custom()
        self.assertIsInstance(validator, AbstractValidator)

    def test_raise_on_bad_validation_result(self):
        """ Raise if validator returns bad type of result """
        class Custom(AbstractValidator):
            def validate(self, value, model=None, context=None):
                return 'Error'

        with self.assertRaises(InvalidErrorType):
            validator = Custom()
            validator.run('some value')




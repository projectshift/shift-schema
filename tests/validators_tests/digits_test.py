from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.validators import Digits
from shiftschema.exceptions import InvalidOption


@attr('validator', 'digits')
class DigitsTest(TestCase):

    def test_create(self):
        """ Can instantiate choice validator """
        validator = Digits()
        self.assertIsInstance(validator, Digits)

    def test_validate_a_copy_of_value(self):
        """ Create a copy of value for validation """
        value = 12345
        value_type = type(value)
        validator = Digits()
        validator.validate(value)
        self.assertEqual(value_type, type(value))

    def test_can_fail(self):
        """ Validating digits and failing """
        value = '123r456'
        validator = Digits()
        error = validator.validate(value)
        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)

    def test_can_fail_with_custom_message(self):
        """ Digits validator accepts custom error """
        msg = 'Me is custom error'
        validator = Digits(msg)
        error = validator.validate('123r456')
        self.assertEqual(msg, error.message)

    def test_can_pass(self):
        """ Valid digits input passes validation  """

        validator = Digits()
        error1 = validator.validate('123456')
        error2 = validator.validate(123456)

        self.assertFalse(error1)
        self.assertFalse(error2)


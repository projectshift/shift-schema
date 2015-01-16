from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.validators import Digits
from shiftvalidate.exceptions import InvalidOption


@attr('validator', 'digits')
class DigitsTest(TestCase):

    def test_create(self):
        """ Can instantiate choice validator """
        validator = Digits()
        self.assertIsInstance(validator, Digits)

    def test_can_fail(self):
        """ Validating digits and failing """
        value = '123r456'
        validator = Digits()
        result = validator.validate(value)
        self.assertFalse(result)
        self.assertTrue(type(result.error) is str)


    def test_can_fail_with_custom_message(self):
        """ Digits validator accepts custom error """
        error = 'Me is custom error'
        validator = Digits(error)
        result = validator.validate('123r456')
        self.assertEqual(error, result.error)


    def test_can_pass(self):
        """ Valid digits input passes validation  """

        validator = Digits()
        result1 = validator.validate('123456')
        result2 = validator.validate(123456)

        self.assertTrue(result1)
        self.assertTrue(result2)
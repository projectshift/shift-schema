from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.validators import Length


@attr('validator', 'length')
class LengthTest(TestCase):
    """ String length validator test"""

    def test_create(self):
        """ Can instantiate length validator """
        validator = Length(min=1, max=10, message='Custom error')
        self.assertIsInstance(validator, Length)


    def test_too_short(self):
        """ Testing if length is too short """
        input = 'Short'
        validator = Length(min=10)
        result = validator.validate(input)

        self.assertFalse(result)
        self.assertTrue(type(result.error) is str)


    def test_too_long(self):
        """ Testing  if length is too long"""
        input = 'Very long string'
        validator = Length(max=3)
        result = validator.validate(input)
        self.assertFalse(result)
        self.assertTrue(type(result.error) is str)


    def test_length_range(self):
        """ Testing length is within range """
        value = 'Me is a very-very long string that is not in range'
        validator = Length(min=3, max=10)
        result = validator.validate(value)
        self.assertFalse(result)
        self.assertTrue(type(result.error) is str)


    def test_return_custom_error(self):
        """ Return custom error on failed validation """
        input = 'Short'
        error = 'Me is custom error'
        validator = Length(min=10, message=error)
        result = validator.validate(input)
        self.assertEqual(error, result.error)


    def test_can_pass_validation(self):
        """ Test that correct length can pass validation """
        value = 'Me is ok'
        validator = Length(min=3, max=8)
        result = validator.validate(value)
        self.assertTrue(result)


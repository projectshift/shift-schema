from unittest import TestCase
from shiftschema.validators import Length


class LengthValidatorTest(TestCase):
    """ String length validator test"""

    def test_create(self):
        """ Can instantiate length validator """
        validator = Length(min=1, max=10, message='Custom error')
        self.assertIsInstance(validator, Length)


    def test_too_short(self):
        """ Testing if length is too short """
        input = 'Short'
        validator = Length(min=10)
        error = validator.run(input)

        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)


    def test_too_long(self):
        """ Testing  if length is too long"""
        input = 'Very long string'
        validator = Length(max=3)
        error = validator.validate(input)
        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)


    def test_length_range(self):
        """ Testing length is within range """
        value = 'Me is a very-very long string that is not in range'
        validator = Length(min=3, max=10)
        error = validator.validate(value)
        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)


    def test_return_custom_error(self):
        """ Return custom error on failed validation """
        input = 'Short'
        msg = 'Me is custom error'
        validator = Length(min=10, message=msg)
        error = validator.validate(input)
        self.assertEqual(msg, error.message)


    def test_can_pass_validation(self):
        """ Test that correct length can pass validation """
        value = 'Me is ok'
        validator = Length(min=3, max=8)
        error = validator.validate(value)
        self.assertFalse(error)


from unittest import TestCase
from shiftschema.validators import NotEmpty


class NotEmptyValidatorTest(TestCase):
    """ Not empty validator test"""

    def test_create(self):
        """ Can instantiate not empty validator """
        validator = NotEmpty(message='Custom error')
        self.assertIsInstance(validator, NotEmpty)

    def test_valid_value_passes(self):
        """ Nonempty iterables pass"""
        validator = NotEmpty()
        error = validator.validate([1, 2, 3])
        self.assertFalse(error)

    def test_invalid_value_fails(self):
        """ Empty iterables fail"""
        validator = NotEmpty()
        error = validator.validate([])
        self.assertTrue(error)
        self.assertEquals('%cant_be_empty%', error.message)

    def test_noniterables_fail(self):
        """ Non-iterables fail not empty test"""
        validator = NotEmpty()
        error = validator.validate(1)
        self.assertTrue(error)
        self.assertEquals('%not_iterable%', error.message)

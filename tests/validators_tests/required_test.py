from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.validators import Required


@attr('validator', 'required')
class RequiredTest(TestCase):
    """ Required validator test"""

    def test_create(self):
        """ Can instantiate required validator """
        validator = Required(message='Custom error')
        self.assertIsInstance(validator, Required)

    def test_valid_value_passes(self):
        """ Valid value passes required check """
        validator = Required()
        error = validator.validate('i am a value')
        self.assertFalse(error)

    def test_empty_values_fail_required_check(self):
        """ Empty values fail required checks """

        # None
        validator = Required()
        error = validator.validate(None)
        self.assertTrue(error)
        self.assertTrue(error.message)

        # False
        validator = Required()
        error = validator.validate(False)
        self.assertTrue(error)
        self.assertTrue(error.message)

        # empty string
        validator = Required()
        error = validator.validate('')
        self.assertTrue(error)
        self.assertTrue(error.message)

        # empty spaces pass
        validator = Required()
        error = validator.validate('     ')
        self.assertFalse(error)

    def test_false_values_can_be_allowed(self):
        """ False can be a valid value for required check """
        validator = Required(allow_false=True)
        error = validator.validate(False)
        self.assertFalse(error)

    def test_zero_values_can_be_allowed(self):
        """ False can be a valid value for required check """
        validator = Required(allow_zero=True)
        error = validator.validate(0)
        self.assertFalse(error)

    def test_empty_strings_can_be_allowed(self):
        """ Empty string can be a valid value for required check """
        validator = Required(allow_empty_string=True)
        error = validator.validate('')
        self.assertFalse(error)

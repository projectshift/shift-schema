from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.validators import Required


@attr('validator', 'required')
class RequiredTest(TestCase):
    """ Required validator test"""

    def test_create(self):
        """ Can instantiate email validator """
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

        # empty strings
        validator = Required()
        error = validator.validate('     ')
        self.assertTrue(error)
        self.assertTrue(error.message)

    def test_false_values_can_be_allowed(self):
        """ False can be a valid value for required check """
        validator = Required(allow_false=True)
        error = validator.validate(False)
        self.assertFalse(error)

from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftvalidate.validators import Choice
from shiftvalidate.exceptions import InvalidOption


@attr('validator', 'choice')
class ChoiceTest(TestCase):
    """ Choice validator test"""

    def test_create(self):
        """ Can instantiate choice validator """
        validator = Choice(['one', 'two', 'three'], message='Custom error')
        self.assertIsInstance(validator, Choice)

    def test_raise_if_choices_not_iterable(self):
        """ Raise an exception if choices not interable """
        with self.assertRaises(InvalidOption):
            Choice(123)


    def test_fail_if_not_in_choises(self):
        """ Fail validation if value not in choices """
        value = 'four'
        validator = Choice(['one', 'two', 'three'])
        result = validator.validate(value)

        self.assertFalse(result)
        self.assertTrue(type(result.error) is str)


    def test_fail_with_custom_error_message(self):
        """ Can fail with custom error message """
        error = 'Custom error'
        validator = Choice(['one', 'two', 'three'], message=error)
        result = validator.validate('four')
        self.assertEqual(error, result.error)


    def test_can_validate_and_pass(self):
        """ Valid value passes validation """
        validator = Choice('spam')
        self.assertTrue(validator.validate('s')) # s in spam

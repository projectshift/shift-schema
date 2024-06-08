from unittest import TestCase
from shiftschema.validators import MultiChoice
from shiftschema.exceptions import InvalidOption


class ChoiceValidatorTest(TestCase):
    """ Choice validator test"""

    def test_create(self):
        """ Can instantiate choice validator """
        validator = MultiChoice(['one', 'two', 'three'], message='Custom error')
        self.assertIsInstance(validator, MultiChoice)

    def test_raise_if_choices_not_iterable(self):
        """ Raise an exception if choices not iterable """
        with self.assertRaises(InvalidOption):
            MultiChoice(123)

    def test_fail_if_not_in_choises(self):
        """ Fail validation if value not in choices """
        value = ['one', 'two', 'four', 'seventeen']
        validator = MultiChoice(['one', 'two', 'three'])
        error = validator.run(value)

        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)
        self.assertIn('four', error.kwargs['items'])
        self.assertIn('seventeen', error.kwargs['items'])

    def test_fail_with_custom_error_message(self):
        """ Can fail with custom error message """
        value = ['one', 'two', 'four', 'seventeen']
        msg = 'Custom error'
        validator = MultiChoice(['one', 'two', 'three'], message=msg)
        error = validator.run('four')
        self.assertEqual(msg, error.message)

    def test_can_validate_and_pass(self):
        """ Valid value passes validation """
        value = ['one', 'two', 'four']
        validator = MultiChoice(value)
        error = validator.run(value)
        self.assertFalse(error)



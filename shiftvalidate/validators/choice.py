from shiftvalidate.validators.abstract_validator import AbstractValidator
from shiftvalidate.results import SimpleResult as Result
from shiftvalidate.exceptions import InvalidOption

class Choice(AbstractValidator):
    """
    Choice validator
    Checks if provided value exists in an iterable of valid choices provided
    at construction time
    """

    invalid_choice = 'Provided value is not a valid choice'


    def __init__(self, valid_choices=None, message=None):
        """
        Initialize validator
        Accepts an iterable of valid choices to check against.

        :param min:             int or None, minimum length
        :param max:             int or None, maximum length
        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.invalid_choice = message

        try:
            iter(valid_choices)
        except TypeError:
            raise InvalidOption('Choices must be an iterable')

        self.choices = valid_choices


    def validate(self, value, context=None):
        """
        Validate
        Perform value validation against validation settings and return
        simple result object

        :param value:           str, value to check
        :param context:         object or None, validation context
        :return:                shiftvalidate.results.SimpleResult
        """

        if value not in self.choices:
            return Result(self.invalid_choice)

        # success otherwise
        return Result()



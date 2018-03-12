from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from shiftschema.exceptions import InvalidOption


class Choice(AbstractValidator):
    """
    Choice validator
    Checks if provided value exists in an iterable of valid choices provided
    at construction time
    """

    invalid_choice = '%choice_not_valid%'

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
        error object.

        :param value:           str, value to check
        :param context:         object or None, validation context
        :return:                shiftschema.result.Error
        """

        if value not in self.choices:
            return Error(self.invalid_choice)

        # success otherwise
        return Error()



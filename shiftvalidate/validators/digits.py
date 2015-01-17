from shiftvalidate.validators.abstract_validator import AbstractValidator
from shiftvalidate.result import Error
from shiftvalidate.exceptions import InvalidOption



class Digits(AbstractValidator):
    """
    Digits validator
    Validates that passed in value consists only of digits.
    """

    not_digital = 'Must only consist of digits.'

    def __init__(self, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.not_digital = message


    def validate(self, value, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check, cast to string
        :param context:         object or None, validation context
        :return:                shiftvalidate.results.SimpleResult
        """
        import re

        value = str(value)
        match = re.match(r'^\d+', value)
        if not match or value != match.group():
            return Error(self.not_digital)

        # success otherwise
        return Error()


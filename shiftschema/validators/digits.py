from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error


class Digits(AbstractValidator):
    """
    Digits validator
    Validates that passed in value consists only of digits.
    """

    not_digital = '%digits_must_only_contain_digits%'

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
        :return:                shiftschema.results.SimpleResult
        """
        import re

        value = str(value)
        match = re.match(r'^\d+', value)
        if not match or value != match.group():
            return Error(self.not_digital)

        # success otherwise
        return Error()



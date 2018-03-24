from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error


class Required(AbstractValidator):
    """
    Required validator
    Checks that provided value is not empty. Typically operates on strings,
    but has an option to consider False as a valid value.
    """

    value_required = '%value_required%'
    allow_false = False

    def __init__(self, allow_false=False, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param message:         str, custom error message
        :param message:         bool, whether to allow False as value
        :return:                None
        """
        self.allow_false = allow_false
        if message is not None:
            self.value_required = message

    def validate(self, value, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """

        # non-empty
        if value and value.strip() != '':
            return Error()

        # false, which is allowed
        if value is False and self.allow_false:
            return Error()

        # error otherwise
        return Error(self.value_required)




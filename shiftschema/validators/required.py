from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error


class Required(AbstractValidator):
    """
    Required validator
    Checks that value was provided. Can operate on strings or entities with an
    option to allow False to be a valid value.
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

        # ok if non-empty string
        if type(value) is str:
            value = value.strip()
            if value != '':
                return Error()

        # ok if has value
        if value:
            return Error()

        # ok if false, but false is allowed
        if value is False and self.allow_false:
            return Error()

        # error otherwise
        return Error(self.value_required)




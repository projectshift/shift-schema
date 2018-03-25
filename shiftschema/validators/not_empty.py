from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from collections import Iterable


class NotEmpty(AbstractValidator):
    """
    Not empty validator
    Checks that provide iterable value is not empty.
    """

    not_iterable = '%not_iterable%'
    cant_be_empty = '%cant_be_empty%'

    def __init__(self, message=None):
        """
        Initialize validator
        Accepts an optional custom can't be empty message

        :param messages:         str, dict, custom error message or dict
        :return:                None
        """
        # if message is not None:
        #     self.cant_be_empty = message
        pass

    def validate(self, value, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check
        :param context:         object or None, validation context
        :return:                shiftschema.results.Error
        """

        if not isinstance(value, Iterable):
            return Error(self.not_iterable)

        try:
            next(iter(value))
        except StopIteration:
            return Error(self.cant_be_empty)

        return Error()




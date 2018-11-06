from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import re


class Url(AbstractValidator):
    """
    URL validator
    """

    not_email = '%url_invalid%'

    def __init__(self, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.not_email = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check
        :param model:           parent model being validated
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """



        # success otherwise
        return Error()


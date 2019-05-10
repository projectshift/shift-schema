from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import ipaddress


class Ip(AbstractValidator):
    """
    IP validator
    Validates that passed in value is a valid IPv4 or IPv6 address
    """

    invalid_ip = '%invalid_ip%'

    def __init__(self, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.invalid_ip = message

    def validate(self, value, model=None, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check, cast to string
        :param model:           parent model being validated
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """

        try:
            ip = ipaddress.ip_address(value)
        except ValueError:
            return Error(self.invalid_ip)

        # success otherwise
        return Error()



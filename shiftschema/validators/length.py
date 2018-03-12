from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error


class Length(AbstractValidator):
    """
    Length validator
    Validates an input for being proper length. You can check for minimum
    length, maximum length or both.
    """

    too_long = '%length_too_long%'
    too_short = '%length_too_short%'
    not_in_range = '%length_not_in_range%'

    def __init__(self, min=None, max=None, message=None):
        """
        Initialize validator
        Accepts minimum and maximum length to check against. Allows only
        single value to be provided.

        :param min:             int or None, minimum length
        :param max:             int or None, maximum length
        :param message:         str, custom error message
        :return:                None
        """
        self.min = min
        self.max = max
        if message is not None:
            self.too_long = message
            self.too_short = message
            self.not_in_range = message

    def validate(self, value, context=None):
        """
        Validate
        Perform value validation against validation settings and return
        simple result object

        :param value:           str, value to check
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """

        length = len(str(value))
        params = dict(min=self.min, max=self.max)

        # too short?
        if self.min and self.max is None:
            if length < self.min:
                return Error(self.too_short, params)

        # too long?
        if self.max and self.min is None:
            if length > self.max:
                return Error(self.too_long, params)

        # within range?
        if self.min and self.max:
            if length < self.min or length > self.max:
                return Error(self.not_in_range, params)

        # success otherwise
        return Error()


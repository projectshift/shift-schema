from shiftvalidate.validators.abstract_validator import AbstractValidator
from shiftvalidate.results import SimpleResult as Result

class Length(AbstractValidator):

    too_long = 'String is too long. Expected length is %s'
    too_short = 'String is too short. Expected length is %s'
    not_in_range = 'String length not in range of min = %s and max = %s'


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
        :return:                shiftvalidate.results.SimpleResult
        """

        length = len(str(value))

        # too short?
        if self.min and self.max is None:
            if length < self.min:
                return Result(False, self.too_short)

        # too long?
        if self.max and self.min is None:
            if length > self.max:
                return Result(False, self.too_long)

        # within range?
        if self.min and self.max:
            if length < self.min or length > self.max:
                return Result(False, self.not_in_range)

        # success otherwise
        return Result(True)


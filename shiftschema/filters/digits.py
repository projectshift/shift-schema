from shiftschema.filters import AbstractFilter
import re


class Digits(AbstractFilter):
    """
    Digits filter
    Removes everything from the string leaving just the digits and optionally
    convert to integer.
    """

    def __init__(self, to_int=False):
        """
        Initialize digits filter. Sets flag to also convert to integer.

        :param to_int:          bool, convert result to integer
        :return:                None
        """
        self.to_int = to_int

    def filter(self, value, model=None, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:           input value
        :param model:           parent model being validated
        :param context:         object, filtering context
        :return:                filtered value
        """

        # string filter: skip non-strings
        if type(value) is not str:
            return value

        pattern = r'\d+'
        found = ''.join(re.findall(pattern, value))

        if found and self.to_int:
            found = int(found)

        return found




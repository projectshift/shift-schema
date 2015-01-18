from shiftschema.filters import AbstractFilter
from shiftschema.exceptions import UnsupportedValueType
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


    def filter(self, value, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:           input value
        :param context:         object, filtering context
        :return:                filtered value
        """

        if not type(value) is str:
            raise UnsupportedValueType('Invalid type of value str expected')

        pattern = r'\d+'
        found = ''.join(re.findall(pattern, value))

        if found and self.to_int:
            found = int(found)

        return found




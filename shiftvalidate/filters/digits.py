from shiftvalidate.filters import AbstractFilter
from shiftvalidate.exceptions import UnsupportedValueType
import re

class Digits(AbstractFilter):
    """
    Digits filter
    Removes everything from the string leaving just the digits
    """
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
        return found




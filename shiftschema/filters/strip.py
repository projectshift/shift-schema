from shiftschema.filters import AbstractFilter
from shiftschema.exceptions import UnsupportedValueType, InvalidOption


class Strip(AbstractFilter):
    """
    Strip filter
    Removes spaces and newlines or specified characters from string.
    Either from the front, back or from both sides.
    """

    def __init__(self, mode='both', chars=None):
        """
        Initialize filter
        Accepts a number of modifiers to specify strip mode (left, right, both)
        and possible optional characters to strip. By default strips
        whitespaces and tabs from both sides.

        :param mode:                string, strip mode
        :param chars:               string or None, characters to strip
        :return:                    None
        """
        modes = ['left', 'right', 'both']
        if mode not in modes:
            raise InvalidOption('Allowed strip modes are left, right or both')

        self.mode = mode
        self.chars = None
        if chars:
            self.chars = str(chars)

    def filter(self, value, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param context:             object, filtering context
        :return:                    filtered value
        """
        if not type(value) is str:
            raise UnsupportedValueType('Invalid type of value str expected')

        if self.mode == 'left':
            return value.lstrip(self.chars)
        elif self.mode == 'right':
            return value.rstrip(self.chars)
        else:
            return value.strip(self.chars)



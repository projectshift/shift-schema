from shiftschema.filters import AbstractFilter
import re


class Stringify(AbstractFilter):
    """
    Stringify filter
    Converts incoming value to string. Use this filter before any others that
    expect a string value
    """

    none_to_int = False
    false_to_empty = False

    def __init__(self, none_to_empty=False, false_to_empty=False):
        """
        Initialize  filter. Sets flag to also convert to integer.

        :param none_to_empty:   bool, convert None to '' (empty string)
        :param false_to_empty:  bool, convert False to '' (empty string)
        :return:                None
        """
        self.none_to_empty = none_to_empty
        self.false_to_empty = false_to_empty

    def filter(self, value, model=None, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:           input value
        :param model:           parent model being validated
        :param context:         object, filtering context
        :return:                filtered value
        """
        if self.none_to_empty and value is None:
            return ''

        if self.false_to_empty and value is False:
            return ''

        return str(value)




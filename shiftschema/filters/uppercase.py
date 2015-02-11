from shiftschema.filters import AbstractFilter
from shiftschema.exceptions import UnsupportedValueType, InvalidOption


class Uppercase(AbstractFilter):
    """
    Uppercase filter
    Converts incoming string to uppercase. If incoming data is not
    a string it will be converted to one implicitly.
    """

    def filter(self, value, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param context:             object, filtering context
        :return:                    filtered value
        """
        value = str(value)
        return value.upper()



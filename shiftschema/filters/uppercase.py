from shiftschema.filters import AbstractFilter


class Uppercase(AbstractFilter):
    """
    Uppercase filter
    Converts incoming string to uppercase. If incoming data is not
    a string it will be converted to one implicitly.
    """

    def filter(self, value, model=None, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param model:               parent model being validated
        :param context:             object, filtering context
        :return:                    filtered value
        """

        # string filter: skip non-strings
        if type(value) is not str:
            return value

        return value.upper()



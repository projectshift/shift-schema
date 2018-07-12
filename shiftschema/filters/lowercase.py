from shiftschema.filters import AbstractFilter


class Lowercase(AbstractFilter):
    """
    Lowercase filter
    Converts incoming string to lowercase. If incoming data is not
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
        value = str(value)
        return value.lower()



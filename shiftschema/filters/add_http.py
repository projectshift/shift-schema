from shiftschema.filters import AbstractFilter


class AddHttp(AbstractFilter):
    """
    Add HTTP
    Adds http to a string if it doesn't start with http or https already.
    """

    def __init__(self, to_int=False):
        """
        Initialize filter.

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
        http = ['http://', 'https://']
        if all(not str(value).startswith(s) for s in http):
            value = 'http://{}'.format(value)

        return value




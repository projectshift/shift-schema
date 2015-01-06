from shiftvalidate.filters.abstract_filter import AbstractFilter


class Strip(AbstractFilter):

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
        if not mode in modes:
            raise ValueError('Allowed strip modes are left, right or both')

        self.mode = mode
        self.chars = None
        if chars:
            self.chars = str(chars)



    def filter(self, value):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:           input value
        :return:                filtered value
        """
        if not type(value) is str:
            raise TypeError('Invalid type of value str expected')

        if self.mode == 'left':
            return value.lstrip(self.chars)
        elif self.mode == 'right':
            return value.rstrip(self.chars)
        else:
            return value.strip(self.chars)



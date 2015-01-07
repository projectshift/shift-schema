
class SimpleResult:
    """
    Simple result
    Represents result of a single check against a validator. This is
    a boolean object that evaluates to True or False but also hold one or
    several validation error messages.
    """
    def __init__(self, valid=False, errors=None):
        """
        Initialize the result
        Sets boolean result status and an optional error message

        :param valid:       bool, result
        :param error:       string or iterable of error messages (optional)
        :return:            None
        """
        self.valid = valid
        if type(errors) is str:
            self.errors = [errors]
        elif errors is not None:
            self.errors = list(errors)


    def __bool__(self):
        """
        Returns boolean status
        :return:            bool
        """
        return bool(self.valid)


    def __eq__(self, other):
        """
        Equals
        Perform equality check. Usually used in boolean checks.

        :param other:       value to compare to
        :return:            bool, comparison result
        """
        return  self.valid == other


    def __neq__(self, other):
        """
        Not equals
        Perform equality check. Usually used in boolean checks.

        :param other:       value to compare to
        :return:            bool, comparison result
        """
        return  self.valid != other
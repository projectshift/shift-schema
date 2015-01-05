
class SimpleResult:
    """
    Simple result
    Represents result of a single check against a validator. This is
    a boolean object that evaluates to True or False but also hold
    validation error message.
    """
    def __init__(self, valid=False, error=None):
        """
        Initialize the result
        Sets boolean result status and an optional error message

        :param valid:       bool, result
        :param error:       string, error message (optional)
        :return:            None
        """
        self.valid = valid
        self.error = error


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
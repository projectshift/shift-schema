
class SimpleResult:
    """
    Simple result
    Represents result of a single check against a validator. This is
    a boolean object that evaluates to True or False but also hold one or
    several validation error messages.
    """
    def __init__(self, errors=None):
        """
        Initialize the result
        Sets boolean result status and an optional error message

        :param valid:       bool, result
        :param error:       string or iterable of error messages (optional)
        :return:            None
        """
        self.errors = []
        if type(errors) is str:
            self.errors = [errors]
        elif errors is not None:
            self.errors = list(errors)


    def __bool__(self):
        """
        Returns boolean status
        :return:            bool
        """
        return len(self.errors) == 0


    def __eq__(self, other):
        """
        Equals
        Perform equality check. Usually used in boolean checks.

        :param other:       value to compare to
        :return:            bool, comparison result
        """
        return  self.__bool__() == other


    def __neq__(self, other):
        """
        Not equals
        Perform equality check. Usually used in boolean checks.

        :param other:       value to compare to
        :return:            bool, comparison result
        """
        return  self.__bool__() != other



class ValidationResult:
    pass

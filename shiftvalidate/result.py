class Error:
    """
    Error
    Represents a single validation check result that evaluates to bool to
    indicate whether the result is valid. In case it's not wil hold the
    error message and optional kwargs for parametrized translation.
    """
    def __init__(self, error=None, kwargs=None):
        self.error = error
        self.kwargs = kwargs

    def __bool__(self):
        return self.error is not None

    def __eq__(self, other):
        return self.__bool__() == other

    def __neq__(self, other):
        return self.__bool__() != other

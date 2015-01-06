
class ShiftValidateException(Exception):
    """
    Main exception category
    All package exceptions extend that to allow you to catch exception by
    component in a general way
    """
    pass


class PropertyExists(ShiftValidateException, ValueError):
    """
    Property exists
    Exception indicates certain property already exists on processor/validator
    """
    pass


class InvalidValidator(ShiftValidateException, TypeError):
    """
    Invalid validator
    Raised when trying to add to processor a validator that does not extend
    from abstract base validator
    """
    pass


class InvalidFilter(ShiftValidateException, TypeError):
    """
    Invalid filter
    Raised when trying to add to processor a filter that does not extend
    from abstract base filter
    """
    pass

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
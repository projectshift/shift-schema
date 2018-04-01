
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


class InvalidErrorType(ShiftValidateException, TypeError):
    """
    Invalid error
    Raised when using strings instead of Error objects
    """
    pass


class InvalidResultType(ShiftValidateException, TypeError):
    """
    Invalid result
    Raised when using invalid validation result objects
    """
    pass


class InvalidSchemaType(ShiftValidateException, TypeError):
    """
    Invalid schema
    Raised when trying to nest schema of bad type in property
    """
    pass


class UnableToMergeResultsType(ShiftValidateException, TypeError):
    """
    Unable to merge results
    Raised when merging to validation result objects into each other, when
    both have the same property but property types do not match, e.g. trying to
    merge simple errors onto nested schema errors
    """
    pass

class InvalidOption(ShiftValidateException, ValueError):
    """
    Invalid exists
    Indicates an invalid option or option value passed to filter or validator
    """
    pass


class UnsupportedValueType(ShiftValidateException, TypeError):
    """
    UnsupportedValueType
    Raised on an attempt to process value of unsupported type. Used mostly
    by filter and validators.
    """
    pass


class NoTranslations(ShiftValidateException, ValueError):
    """
    Translation not found
    Indicates that no translation dictionary exists in registered path
    for the locale provided
    """
    pass
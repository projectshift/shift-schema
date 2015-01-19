from pprint import pformat
from copy import deepcopy
from shiftschema.exceptions import InvalidErrorType, InvalidResultType

class Error:
    """
    Error
    Represents a single validation check result that evaluates to bool to
    indicate whether the result is valid. In case it's not wil hold the
    error message and optional kwargs for parametrized translation.
    """
    def __init__(self, message=None, kwargs=None):
        """
        Initialize
        Accepts error message and optional iterable of parameters used to
        format at translation time.

        :param message:             str or None
        :param kwargs:              iterable or None
        :return:                    None
        """
        self.message = message
        self.kwargs = kwargs

    def __bool__(self):
        return self.message is not None

    def __eq__(self, other):
        return self.__bool__() == other

    def __ne__(self, other):
        return self.__bool__() != other

    def __repr__(self):
        r = '<{} object message="{}">'
        return r.format(self.__class__.__qualname__, self.message)

class Result:
    """
    Result
    Represents result of validating with a schema. Contains properties and
    their errors but can also contain nested results for nested schemas.
    """
    def __init__(self, errors=None, translator=None, locale='en'):
        if not errors:
            errors = dict()
        self.errors = errors
        self.translator = translator
        self.locale=locale

    def __bool__(self):
        return not self.errors

    def __eq__(self, other):
        return self.__bool__() == other

    def __ne__(self, other):
        return self.__bool__() != other

    def __repr__(self):
        return pformat(self.errors)

    def add_errors(self, errors, property_name=None):
        """ Add one or several errors """
        if type(errors) is not list:
            errors = [errors]
        for error in errors:
            if not isinstance(error, Error):
                err = 'Error must be of type {}'
                raise InvalidErrorType(err.format(Error))

        if property_name:
            if property_name in self.errors:
                self.errors[property_name].extend(errors)
            else:
                self.errors[property_name] = errors
        else:
            if '__state__' in self.errors:
                self.errors['__state__'].extend(errors)
            else:
                self.errors['__state__'] = errors

    def add_nested_errors(self, errors, property_name):
        """ Attach aggregate of errors to a property"""
        if isinstance(errors, Result):
            errors = errors.errors
        self.errors[property_name] = errors

    def merge(self, another):
        """ Merge another result into itself"""
        if not isinstance(another, Result):
            err = 'Unable to merge: must be "{}", got "{}"'
            raise InvalidResultType(err.format(Result, another))

        errors = another.errors
        for property_name in errors:
            if property_name in self.errors:
                self.errors[property_name].extend(errors[property_name])
            else:
                self.errors[property_name] = errors[property_name]
                
    def get_messages(self, locale=None):
        """ Get a dictionary of translated messages """
        if locale is None:
            locale = self.locale

        if self.translator:
            def translate(error):
                return self.translator.translate(error, locale)
        else:
            def translate(error):
                return error

        errors = deepcopy(self.errors)
        errors = self._translate_errors(errors, translate)
        return errors

    def _translate_errors(self, errors, translate):
        """ Recursively apply translate callback to each error message"""
        for property_name in errors:
            property_errors = errors[property_name]
            if type(property_errors) is list:
                for index,error in enumerate(property_errors):
                    message = translate(error.message)
                    message = self.format_error(message, error.kwargs)
                    errors[property_name][index] = message
            elif type(property_errors) is dict:
                errors[property_name] = self._translate_errors(
                    property_errors, translate
                )

        return errors

    def format_error(self, error, args=None):
        """ Format error with positional or named arguments (if any) """
        if type(args) is dict:
            return error.format(**args)
        if type(args) is list or type(args) is tuple:
            return error.format(*args)

        return error







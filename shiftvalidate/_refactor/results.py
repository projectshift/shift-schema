from shiftvalidate.exceptions import InvalidErrorType

class SimpleResult:
    """
    Simple result
    Represents a result of performing single validation check. Evaluates
    to True in case of no errors. May contain error message/code and
    an optional set of kwargs to be used at translation.
    """
    def __init__(self, error=None, kwargs=None):
        """
        Initialize the result
        Sets error message and optional dynamic kwargs for formatting and
        translations.

        :param error:           str or None, error message
        :return:                None
        """
        self.error = error
        self.kwargs = kwargs

    def __bool__(self):
        """ Evaluate to boolean """
        return self.error is None

    def __eq__(self, other):
        """ Compare to value """
        return self.__bool__() == other


    def __ne__(self, other):
        """ Compare to value """
        return  self.__bool__() != other


class ValidationResult:
    """
    Validation result
    Represents a result of schema validation to an entity.
    Usually holds a list of properties and their corresponding errors but can
    as well a number of state validation results (applied to entity as whole)
    that have no property name. Supports merging of several objects together
    for complex aggregate validations.
    """

    def __init__(self):
        self.errors = {}


    def __bool__(self):
        """
        Returns boolean status
        :return:            bool
        """
        return not self.errors


    def __eq__(self, other):
        """
        Equals
        Perform equality check. Usually used in boolean checks.

        :param other:           value to compare to
        :return:                bool, comparison result
        """
        return self.__bool__() == other


    def __ne__(self, other):
        """
        Not equals
        Perform equality check. Usually used in boolean checks.

        :param other:           value to compare to
        :return:                bool, comparison result
        """
        return  self.__bool__() != other


    def add_errors(self, errors, property_name=None):
        """
        Add errors
        Accepts one or more error messages to attach possibly with related
        property name or without any for state validation errors.

        :param errors:          SimpleResult or a list of those
        :param property_name:   string, property name
        :return:                None
        """

        # check errors
        exception = 'Error must be a SimpleResult or a list of those'
        if not isinstance(errors, SimpleResult) and type(errors) is not list:
            raise InvalidErrorType(exception)
        elif type(errors) is list:
            for error in errors:
                if not isinstance(error, SimpleResult):
                    raise InvalidErrorType(exception)

        # convert to list
        if isinstance(errors, SimpleResult):
            errors = [errors]

        # add property errors
        if property_name:
            if property_name in self.errors:
                self.errors[property_name].extend(errors)
            else:
                self.errors[property_name] = errors

        # add state errors
        else:
            if '__state__' in self.errors:
                self.errors['__state__'].extend(errors)
            else:
                self.errors['__state__'] = errors


    def add_nested_errors(self, property_name, errors):
        """
        Add nested error set
        Attaches an aggregate of errors to a property. Such an aggregate
        usually results from a nestend entity validation.

        :param property_name:       string, property name
        :param errors:              dict, ValidationResult, error set to attach
        :return:                    None
        """
        if isinstance(errors, ValidationResult):
            errors = errors.errors
        self.errors[property_name] = errors


    def merge(self, validation_result):
        """
        Merge
        Merges two validation result objects together.

        :param validation_result:   shiftvalidate.results.ValidationResult
        :return:                    None
        """
        if not isinstance(validation_result, ValidationResult):
            raise TypeError('Unable to merge: must be ValidationResult object')

        errors = validation_result.errors
        for property_name in errors:
            if property_name in self.errors:
                self.errors[property_name].extend(errors[property_name])
            else:
                self.errors[property_name] = errors[property_name]


    def __repr__(self):
        """
        Printable version of errors

        :return:                    string
        """
        from pprint import pformat
        return pformat(self.errors)






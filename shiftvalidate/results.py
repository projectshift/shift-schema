
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

        :param valid:           bool, result
        :param error:           string or iterable of error messages (optional)
        :return:                None
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

        :param other:           value to compare to
        :return:                bool, comparison result
        """
        return self.__bool__() == other


    def __neq__(self, other):
        """
        Not equals
        Perform equality check. Usually used in boolean checks.

        :param other:           value to compare to
        :return:                bool, comparison result
        """
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


    def __neq__(self, other):
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

        :param errors:          string or list
        :param property_name:   string, property name
        :return:                None
        """

        # convert to list
        if type(errors) is str:
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


    def translate_errors(self, errors, translator):
        """
        Translate errors
        Recursively goes through a dictionary of errors and applies passed
        translator to each error.

        :param errors:              dict, nested error set
        :param translator:          function, translation func
        :return:                    dict
        """
        for property in errors:
            property_errors = errors[property]

            if type(property_errors) is list:
                for index, error in enumerate(property_errors):
                    errors[property][index] = translator(error)
            elif type(property_errors) is dict:
                errors[property] = self.translate_errors(
                    property_errors,
                    translator
                )

        return errors




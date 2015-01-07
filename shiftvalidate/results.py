
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


    def add_errors(self, property=None, errors=None, debug=False):
        """
        Add errors
        Accepts one or more error messages to attache possibly with related
        property name or without any for state validation errors.

        :param property:        string, property name
        :param errors:          string, list or aggregate dict of errors
        :return:                None
        """

        # convert single error to list
        if type(errors) is str:
            errors = [errors]

        # create aggregate if list
        aggregate = {}
        if type(errors) is list:
            if property:
                aggregate[property] = errors
            else:
                aggregate['__state__'] = errors

        # already an aggregate?
        if type(errors) is dict:
            aggregate = errors

        # now process aggregate
        for index in aggregate.keys():
            if index not in self.errors:
                self.errors[index] = aggregate[index] # set
            else:
                self.errors[index].extend(aggregate[index]) # or append


    def merge(self, validation_result):
        """
        Merge
        Merges two validation result objects together.

        :param validation_result:   shiftvalidate.results.ValidationResult
        :return:                    None
        """
        if not isinstance(validation_result, ValidationResult):
            raise TypeError('Unable to merge: must be ValidationResult object')

        self.add_errors(errors=validation_result.errors)
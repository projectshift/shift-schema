from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters.abstract_filter import AbstractFilter
from shiftvalidate.validators.abstract_validator import AbstractValidator

class Property:
    """
    Property
    Represents a simple single-value property on the processor and
    holds a number of filters and validators for property value
    """

    # property filters
    filters = []

    # property validators
    validators = []


    def add_filter(self, filter):
        """
        Add filter
        Adds a filter to property. All added filters must extend from
        abstract base filter in AbstractFilter and will raise InvalidFilter
        if it does not.

        :param filter:              object, a filter to attach
        :return:                    shiftvalidate.proerties.Property
        """
        if not isinstance(filter, AbstractFilter):
            err = 'Filters must be of type {}'.format(AbstractFilter)
            raise InvalidFilter(err)

        self.filters.append(filter)
        return self


    def add_validator(self, validator):
        """
        Add validator
        Adds a validator to property. All added validators must extend from
        abstract base validator in AbstractValidator and will raise
        InvalidValidator if it does not.

        :param validator:           object, a validator to attach
        :return:                    shiftvalidate.proerties.Property
        """
        if not isinstance(validator, AbstractValidator):
            err = 'Validator must be of type {}'.format(AbstractValidator)
            raise InvalidFilter(err)

        self.validators.append(filter)
        return self



    def filter_value(self, value):
        pass

    def validate_value(self, value):
        pass

    def process_value(self, value):
        pass







class Entity:
    pass

class Collection:
    pass
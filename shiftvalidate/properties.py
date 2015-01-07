from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters import AbstractFilter
from shiftvalidate.validators import AbstractValidator
from shiftvalidate.results import SimpleResult

class Property:
    """
    Property
    Represents a simple single-value property on the processor and
    holds a number of filters and validators for property value
    """
    def __init__(self):
        """
        Initialize
        Defines instance-level container for filters and validators

        :return:                    None
        """
        self.filters = []
        self.validators = []



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
            raise InvalidValidator(err)

        self.validators.append(validator)
        return self



    def filter_value(self, value, context=None):
        """
        Filter value
        Sequentially applies each attached filter to value.

        :param value:               value to filter
        :param context:             object, context (usually an entity)
        :return:                    str, filtered result
        """
        for filter in self.filters:
            value = filter.filter(value, context=context)

        return value



    def validate_value(self, value, context=None):
        """
        Validate value
        Sequentially applies each attached validator and collect error
        messages

        :param value:               value to validate
        :param context:             object, context (usually an entity)
        :return:                    shiftvalidate.results.SimpleResult
        """

        errors = []
        for validator in self.validators:
            ok = validator.validate(value)
            if not ok:
                for error in ok.errors:
                    errors.append(error)

        if errors:
            return SimpleResult(errors)
        else:
            return SimpleResult()










class Entity:
    pass

class Collection:
    pass
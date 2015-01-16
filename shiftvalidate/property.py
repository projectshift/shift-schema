from shiftvalidate.filters import AbstractFilter
from shiftvalidate.validators import AbstractValidator
from shiftvalidate.exceptions import InvalidFilter, InvalidValidator

class SimpleProperty:
    """
    Simple property
    A single value property on the schema and holds a number of filters and
    validators for this value
    """
    def __init__(self):
        self.filters = []
        self.validators = []

    def add_filter(self, filter):
        """
        Add filter to property
        :param filter: object, extending from AbstractFilter
        :return: None
        """
        if not isinstance(filter, AbstractFilter):
            err = 'Filters must be of type {}'.format(AbstractFilter)
            raise InvalidFilter(err)

        if filter not in self.filters:
            self.filters.append(filter)
        return self

    def add_validator(self, validator):
        """
        Add validator to property

        :param validator: object, extending from AbstractValidator
        :return: None
        """
        if not isinstance(validator, AbstractValidator):
            err = 'Validator must be of type {}'.format(AbstractValidator)
            raise InvalidValidator(err)

        self.validators.append(validator)
        return self

    def filter_value(self, value, context=None):
        """
        Sequentially applies all the filters to provided value

        :param value: a value to filter
        :param context: filtering context, usually parent entity
        :return: filtered value
        """
        for filter in self.filters:
            value = filter.filter(value, context=context)

        return value

    def validate_value(self, value, context=None):
        """
        Sequentially apply each validator to value and collect errors.

        :param value: a value to validate
        :param context: validation context, usually parent entity
        :return: list of errors (if any)
        """
        errors = []
        for validator in self.validators:
            error = validator.validate(value, context)
            if error:
                errors.append(error)

        return errors


class EntityProperty:
    pass
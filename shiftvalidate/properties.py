from shiftvalidate.exceptions import InvalidFilter, InvalidValidator
from shiftvalidate.filters import AbstractFilter
from shiftvalidate.validators import AbstractValidator
from shiftvalidate.results import SimpleResult

class Collection:
    """ Collections are not yet implemented """
    pass


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
    """
    Entity
    Represents linked entity existing on a property of another one. Mostly
    used for cases when you need to process a complex entity aggregate
    that is being persisted via cascades. For example a person and a
    linked address entity. Linked entities allow you to arbitrarily nest
    schemas.
    """

    def __init__(self):
        """
        Initialize entity property
        Defines instance-level container for linked entity schema.

        :return:                    None
        """
        self.schema = None

    def set_schema(self, schema):
        """
        Set schema
        Attaches nested schema to filter and liked entity. Will raise
        TypeError if trying to attach something other than schema.

        :param schema:              shiftvalidate.schema.Schema
        :return:                    None
        """
        from shiftvalidate.schema import Schema
        if isinstance(schema, Schema):
            self.schema = schema
            return

        err = 'Linked entity schema must be of type {}'.format(Schema)
        raise TypeError(err)





    def filter(self, model):
        """
        Filter
        Use linked entity schema to filter provided entity.

        :param model:               object, an entity to process
        :return:                    None
        """
        pass


    def validate(self, model):
        """
        Validate
        Use linked entity schema to validate provided entity and return
        ValidationResult object

        :param model:               object, an entity to process
        :return:                    shiftvalidate.results.ValidationResult
        """
        pass


    def process(self, model):
        """
        Process
        Uses linked entity schema to both filter and validate provided entity
        in one go and return ValidationResult object.

        :param model:               object, an entity to process
        :return:                    shiftvalidate.results.ValidationResult
        """
        pass
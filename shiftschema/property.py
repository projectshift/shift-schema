from shiftschema.filters import AbstractFilter
from shiftschema.validators import AbstractValidator
from shiftschema.exceptions import InvalidFilter, InvalidValidator
from shiftschema.exceptions import InvalidSchemaType
from shiftschema.result import Result, Error


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

    def filter(self, value=None, context=None):
        """
        Sequentially applies all the filters to provided value

        :param value: a value to filter
        :param context: filtering context, usually parent entity
        :return: filtered value
        """
        if value is None:
            return
        for filter_obj in self.filters:
            value = filter_obj.filter(value, context=context)
        return value

    def validate(self, value=None, context=None):
        """
        Sequentially apply each validator to value and collect errors.

        :param value: a value to validate
        :param context: validation context, usually parent entity
        :return: list of errors (if any)
        """
        errors = []
        for validator in self.validators:
            error = validator.run(value, context)
            if error:
                errors.append(error)

        return errors


class EntityProperty:
    """
    Entity property
    Used to process linked entities existing on a property. Can have
    filters and validators attached as well as an empty schema.
    """

    def __init__(self, *, required=False):
        self.filters = []
        self.validators = []
        self._required = required
        self._required_message = "%property_required%"
        self._schema = None

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        self._required = bool(value)

    @property
    def required_message(self):
        return self._required_message

    @required_message.setter
    def required_message(self, msg):
        self._required_message = msg

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        from shiftschema.schema import Schema
        if isinstance(schema, Schema):
            self._schema = schema
            return

        err = 'Nested schema must be of type "{}" got "{}"'
        raise InvalidSchemaType(err.format(Schema, schema))

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

    def filter(self, value=None, context=None, third=None):
        """ Perform model filtering with filters attached directly """
        if value is None:
            return

        for filter in self.filters:
            value = filter.filter(value, context)

        return value

    def filter_with_schema(self, value=None, context=None):
        """ Perform model filtering with schema """
        if value is None or self.schema is None:
            return

        self._schema.filter(value, context)

    def validate_with_schema(self, model=None, context=None):
        """ Perform model validation with schema"""

        # validate required (regression: before skipping on no schema)
        if model is None and self.required:
            return [Error(self.required_message)]

        if self._schema is None or (model is None and not self.required):
            return

        result = self._schema.validate(model, context)
        return result



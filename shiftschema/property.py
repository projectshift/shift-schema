from shiftschema.filters import AbstractFilter
from shiftschema.validators import AbstractValidator
from shiftschema.exceptions import InvalidFilter, InvalidValidator
from shiftschema.exceptions import InvalidSchemaType
from shiftschema.validators import Required


class SimpleProperty:
    """
    Simple property
    A single value property on the schema and holds a number of filters and
    validators for this value
    """
    def __init__(self, use_context=True):
        """
        Initialize property
        Can optionally accept a flag indicating whether the property should
        inherit context when being filtered and validated. This is useful
        to control how custom context is being passed down when validating
        graphs with nested schemas.

        :param use_context: bool, use or ignore passed context
        """
        self.filters = []
        self.validators = []
        self.use_context = use_context

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

    def filter(self, value=None, model=None, context=None):
        """
        Sequentially applies all the filters to provided value

        :param value: a value to filter
        :param model: parent entity
        :param context: filtering context, usually parent entity
        :return: filtered value
        """
        if value is None:
            return value
        for filter_obj in self.filters:
            value = filter_obj.filter(
                value=value,
                model=model,
                context=context if self.use_context else None
            )
        return value

    def validate(self, value=None, model=None, context=None):
        """
        Sequentially apply each validator to value and collect errors.

        :param value: a value to validate
        :param model: parent entity
        :param context: validation context, usually parent entity
        :return: list of errors (if any)
        """
        errors = []
        for validator in self.validators:
            if value is None and not isinstance(validator, Required):
                continue

            error = validator.run(
                value=value,
                model=model,
                context=context if self.use_context else None
            )
            if error:
                errors.append(error)

        return errors


class EntityProperty(SimpleProperty):
    """
    Entity property
    Used to process linked entities existing on a property. Can have
    filters and validators attached as well as a nested schema.
    """

    def __init__(self, use_context=True):
        super().__init__(use_context=use_context)
        self._schema = None

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

    def filter_with_schema(self, model=None, context=None):
        """ Perform model filtering with schema """
        if model is None or self.schema is None:
            return

        self._schema.filter(
            model=model,
            context=context if self.use_context else None
        )

    def validate_with_schema(self, model=None, context=None):
        """ Perform model validation with schema"""
        if self._schema is None or model is None:
            return

        result = self._schema.validate(
            model=model,
            context=context if self.use_context else None
        )
        return result


class CollectionProperty(EntityProperty):
    """
    Collection property
    Allows to validate nested collection of entities that exist on a property
    of another entity. Filters and validators will be applied to collection as
    whole, when schema will be applied to each item in the collection.
    """

    def filter_with_schema(self, collection=None, context=None):
        """ Perform collection items filtering with schema """
        if collection is None or self.schema is None:
            return
        for item in collection:
            self._schema.filter(
                model=item,
                context=context if self.use_context else None
            )

    def validate_with_schema(self, collection=None, context=None):
        """ Validate each item in collection with our schema"""
        if self._schema is None or not collection:
            return

        result = []
        for index, item in enumerate(collection):
            item_result = self._schema.validate(
                model=item,
                context=context if self.use_context else None
            )
            result.append(item_result)

        return result






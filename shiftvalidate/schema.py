from shiftvalidate.property import SimpleProperty, EntityProperty
from shiftvalidate.result import Error, Result
from shiftvalidate.filters import AbstractFilter
from shiftvalidate.validators import AbstractValidator
from shiftvalidate.exceptions import InvalidValidator, PropertyExists

class Schema:
    """
    Schema
    Contains rules for filtering and validation of an entity. Can be
    instantiated from spec, configured manually or by extending.
    """

    def __init__(self, spec=None):
        self.state = []
        self.properties = {}
        self.entities = {}

        # create from spec
        if spec:
            self.factory(spec)

        # or by subclassing
        self.schema()

    def schema(self):
        """
        Schema: Implement this in subclasses and configure your rules here
        :return: None
        """
        pass

    def factory(self, spec):
        """
        Factory method: configures itself from a spec dictionary
        :param spec: dict
        :return: None
        """
        if 'state' in spec:
            for state_validator in spec['state']:
                self.add_state_validator(state_validator)

        if 'entities' in spec:
            for property_name in spec['entities']:
                self.add_entity(property_name)
                prop = self.entities[property_name]
                prop_spec = spec['entities'][property_name]

                required = bool(prop_spec.get('required', False))
                if required:
                    prop.required = required

                msg = prop_spec.get('required_message')
                if msg:
                    prop.required_message = msg

                schema = prop_spec.get('schema')
                if schema:
                    prop.schema = schema

        if 'properties' in spec:
            for property_name in spec['properties']:
                self.add_property(property_name)
                prop = self.properties[property_name]
                prop_spec = spec['properties'][property_name]

                required = bool(prop_spec.get('required', False))
                if required:
                    prop.required = required

                msg = prop_spec.get('required_message')
                if msg:
                    prop.required_message = msg

                prop_filters = prop_spec.get('filters')
                if prop_filters:
                    for filter in prop_filters:
                        prop.add_filter(filter)

                prop_validators = prop_spec.get('validators')
                if prop_validators:
                    for validator in prop_validators:
                        prop.add_validator(validator)

    def has_property(self, property_name):
        """
        Check if schema has property
        :param property_name: str, name to check
        :return: bool
        """
        if property_name in self.properties:
            return True
        elif property_name in self.entities:
            return True
        else:
            return False

    def __getattr__(self, property_name):
        """
        Implements property access
        :param property_name: name to get
        :return: obj, property
        """
        if property_name in self.properties:
            return self.properties[property_name]
        elif property_name in self.entities:
            return self.entities[property_name]
        else:
            return object.__getattribute__(self, property_name)

    def add_state_validator(self, validator):
        """
        Add entity state validator
        :param validator: a validator, implementing AbstractValidator
        :return: None
        """
        if not isinstance(validator, AbstractValidator):
            err = '{} is not a subclass of {}'
            raise InvalidValidator(err.format(validator, AbstractValidator))

        if validator not in self.state:
            self.state.append(validator)

    def add_property(self, property_name):
        """
        Add simple property to schema
        :param property_name: str, property name
        :return: None
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))
        self.properties[property_name] = SimpleProperty()

    def add_entity(self, property_name):
        """
        Add entity property to schema
        :param property_name: str, property name
        :return: None
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))
        self.entities[property_name] = EntityProperty()

    def get(self, model, property_name):
        """
        Get property from model. Use getter if possible.
        :param model: model or dict
        :param property_name: str, name on the model
        :return: mixed
        """
        if type(model) is dict and property_name in model:
            return model[property_name]
        elif hasattr(model, 'get_' + property_name):
            getter = getattr(model, 'get_' + property_name)
            return getter()
        else:
            return getattr(model, property_name)

    def set(self, model, property_name, value):
        """
        Set model property to value. Use setter if possible.
        :param model: model object or dict
        :param property_name: str, name on the model
        :param value: mixed, a value to set
        :return: None
        """
        if type(model) is dict:
            model[property_name] = value
        elif hasattr(model, 'set_' + property_name):
            setter = getattr(model, 'set_' + property_name)
            setter(value)
        else:
            setattr(model, property_name, value)

    def process(self, model=None, context=None):
        """
        Perform validation and filtering at the same time, return a
        validation result object.

        :param model: object or dict
        :param context: object, dict or None
        :return: shiftvalidate.result.Result
        """
        self.filter(model, context)
        return self.validate(model, context)

    def filter(self, model=None, context=None):
        """
        Perform filtering on the model. Will change model in place.
        :param model: object or dict
        :param context: object, dict or None
        :return: None
        """
        if model is None:
            return

        # properties
        for property_name in self.properties:
            value = self.get(model, property_name)
            if value is None:
                continue

            property_context = model # simple properties context
            value = self.properties[property_name].filter_value(
                value=value,
                context=property_context
            )
            self.set(model, property_name, value)

        # entities
        for property_name in self.entities:
            entity = self.get(model, property_name)
            if entity is None:
                continue

            entity_ctx = model # nested entities get parent for context
            self.entities[property_name].filter(
                model=entity,
                context=entity_ctx
            )
            # self.set(model, property_name, entity)

    def validate(self, model=None, context=None):
        """
        Validate model and return validation result object
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftvalidate.result.Result
        """
        result = Result()

        # validate state
        for state_validator in self.state:
            state_ctx = context  # none or parent model (for nested schemas)
            error = state_validator.run(model, state_ctx)
            if error:
                result.add_errors(property_name=None, errors=error)

        # validate properties
        for property_name in self.properties:
            value = self.get(model, property_name)
            required = self.properties[property_name].required
            if value is None and not required:
                continue

            property_ctx = model # model for simple properties
            errors = self.properties[property_name].validate_value(
                value=value,
                context=property_ctx
            )
            if errors:
                result.add_errors(errors, property_name)

        # validate linked entities
        for property_name in self.entities:
            entity = self.get(model, property_name)
            required = self.entities[property_name].required
            if entity is None and not required:
                continue

            entity_ctx = model # model for nested entities
            nested_valid = self.entities[property_name].schema.validate(
                model=entity,
                context=entity_ctx
            )

            # required and missing?
            if type(nested_valid) is list:
                result.add_errors(property_name, nested_valid)

            # or is a nested result?
            elif isinstance(nested_valid, Result) and not nested_valid:
                result.add_nested_errors(
                    property_name=property_name,
                    errors=nested_valid.errors
                )

        return result










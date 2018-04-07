from shiftschema.property import SimpleProperty
from shiftschema.property import EntityProperty
from shiftschema.property import CollectionProperty
from shiftschema.result import Result
from shiftschema.validators import AbstractValidator
from shiftschema.exceptions import InvalidValidator, PropertyExists
from shiftschema.translator import Translator


class Schema:
    """
    Schema
    Contains rules for filtering and validation of an entity. Can be
    instantiated from spec, configured manually or by extending.
    """

    locale = 'en'
    translator = Translator()

    def __init__(self, spec=None, locale=None, translator=None):
        self.state = []
        self.properties = {}
        self.entities = {}
        self.collections = {}

        # create from spec
        if spec:
            self.factory(spec)

        if locale:
            self.locale = locale
        if translator:
            self.translator = translator

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

        if 'properties' in spec:
            for property_name in spec['properties']:
                self.add_property(property_name)
                prop = self.properties[property_name]
                prop_spec = spec['properties'][property_name]

                prop_filters = prop_spec.get('filters')
                if prop_filters:
                    for filter in prop_filters:
                        prop.add_filter(filter)

                prop_validators = prop_spec.get('validators')
                if prop_validators:
                    for validator in prop_validators:
                        prop.add_validator(validator)

        if 'entities' in spec:
            for property_name in spec['entities']:
                self.add_entity(property_name)
                prop = self.entities[property_name]
                prop_spec = spec['entities'][property_name]

                prop_filters = prop_spec.get('filters')
                if prop_filters:
                    for filter in prop_filters:
                        prop.add_filter(filter)

                prop_validators = prop_spec.get('validators')
                if prop_validators:
                    for validator in prop_validators:
                        prop.add_validator(validator)

                schema = prop_spec.get('schema')
                if schema:
                    prop.schema = schema

        if 'collections' in spec:
            for property_name in spec['collections']:
                self.add_collection(property_name)
                prop = self.collections[property_name]
                prop_spec = spec['collections'][property_name]

                prop_filters = prop_spec.get('filters')
                if prop_filters:
                    for filter in prop_filters:
                        prop.add_filter(filter)

                prop_validators = prop_spec.get('validators')
                if prop_validators:
                    for validator in prop_validators:
                        prop.add_validator(validator)

                schema = prop_spec.get('schema')
                if schema:
                    prop.schema = schema

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
        elif property_name in self.collections:
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
        elif property_name in self.collections:
            return self.collections[property_name]
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
        :return: shiftschema.property.SimpleProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))

        prop = SimpleProperty()
        self.properties[property_name] = prop
        return prop

    def add_entity(self, property_name):
        """
        Add entity property to schema
        :param property_name: str, property name
        :return: shiftschema.property.EntityProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))
        prop = EntityProperty()
        self.entities[property_name] = prop
        return prop

    def add_collection(self, property_name):
        """
        Add collection property to schema
        :param property_name: str, property name
        :return: shiftschema.property.CollectionProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))

        prop = CollectionProperty()
        self.collections[property_name] = prop
        return prop

    def get(self, model, property_name):
        """
        Get property from model. Use getter if possible.
        :param model: model or dict
        :param property_name: str, name on the model
        :return: mixed
        """
        if type(model) is dict:
            if property_name not in model:
                return None
            else:
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
        :return: shiftschema.result.Result
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
            prop = self.properties[property_name]
            value = self.get(model, property_name)
            if value is None:
                continue

            property_ctx = context if context else model
            filtered_value = prop.filter(value, property_ctx)
            if value != filtered_value:  # unless changed!
                self.set(model, property_name, filtered_value)

        # entities
        for property_name in self.entities:
            prop = self.entities[property_name]
            value = self.get(model, property_name)
            entity_ctx = context if context else model

            filtered_value = prop.filter(value, entity_ctx)
            if value != filtered_value:  # unless changed!
                self.set(model, property_name, filtered_value)

            prop.filter_with_schema(value, entity_ctx)

        # collections
        for property_name in self.collections:
            prop = self.collections[property_name]
            collection = self.get(model, property_name)
            collection_ctx = context if context else model

            filtered_value = prop.filter(collection, collection_ctx)
            self.set(model, property_name, filtered_value)

            prop.filter_with_schema(collection, collection_ctx)

    def validate(self, model=None, context=None):
        """
        Validate model and return validation result object
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftschema.result.Result
        """

        # inject with settings
        result = Result(translator=self.translator, locale=self.locale)

        # validate state
        for state_validator in self.state:
            state_ctx = context  # none or parent model (for nested schemas)
            error = state_validator.run(model, state_ctx)
            if error:
                result.add_state_errors(error)

        # validate simple properties
        for property_name in self.properties:
            value = self.get(model, property_name)
            property_ctx = context if context else model
            errors = self.properties[property_name].validate(
                value=value,
                context=property_ctx
            )

            if errors:
                result.add_errors(errors=errors, property_name=property_name)

        # validate nested entity properties
        for property_name in self.entities:
            prop = self.entities[property_name]
            value = self.get(model, property_name)
            entity_ctx = context if context else model

            errors = prop.validate(value, entity_ctx)
            if len(errors):
                result.add_entity_errors(
                    property_name=property_name,
                    direct_errors=errors
                )

            if value is None:
                continue

            schema_valid = prop.validate_with_schema(value, entity_ctx)
            if schema_valid == False:
                result.add_entity_errors(
                    property_name,
                    schema_errors=schema_valid.errors
                )

        # validate collection properties
        for property_name in self.collections:
            prop = self.collections[property_name]
            collection = self.get(model, property_name)
            collection_ctx = context if context else model

            errors = prop.validate(collection, collection_ctx)
            if len(errors):
                result.add_collection_errors(
                    property_name=property_name,
                    direct_errors=errors
                )

            collection_errors = prop.validate_with_schema(
                collection,
                context # not collection ctx
            )

            result.add_collection_errors(
                property_name=property_name,
                collection_errors=collection_errors
            )

        return result










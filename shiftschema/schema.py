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

    def __init__(self, locale=None, translator=None):
        self.state = []
        self.properties = {}
        self.entities = {}
        self.collections = {}

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

    def add_property(self, property_name, use_context=True):
        """
        Add simple property to schema
        :param property_name: str, property name
        :param use_context: bool, whether custom context should be used
        :return: shiftschema.property.SimpleProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))

        prop = SimpleProperty(use_context=bool(use_context))
        self.properties[property_name] = prop
        return prop

    def add_entity(self, property_name, use_context=True):
        """
        Add entity property to schema
        :param property_name: str, property name
        :param use_context: bool, whether custom context should be used
        :return: shiftschema.property.EntityProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))
        prop = EntityProperty(use_context=bool(use_context))
        self.entities[property_name] = prop
        return prop

    def add_collection(self, property_name, use_context=True):
        """
        Add collection property to schema
        :param property_name: str, property name
        :param property_name: str, property name
        :return: shiftschema.property.CollectionProperty
        """
        if self.has_property(property_name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(property_name))

        prop = CollectionProperty(use_context=bool(use_context))
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
            try:
                return getattr(model, property_name)
            except AttributeError:
                return None

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
            try:
                setattr(model, property_name, value)
            except AttributeError:
                pass

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
        self.filter_properties(model, context=context)

        # entities
        self.filter_entities(model, context=context)

        # collections
        self.filter_collections(model, context=context)

    def filter_properties(self, model, context=None):
        """
        Filter simple properties
        Runs filters on simple properties changing them in place.
        :param model:  object or dict
        :param context: object, dict or None
        :return: None
        """
        if model is None:
            return

        for property_name in self.properties:
            prop = self.properties[property_name]
            value = self.get(model, property_name)
            if value is None:
                continue

            filtered_value = prop.filter(
                value=value,
                model=model,
                context=context
            )
            if value != filtered_value:  # unless changed!
                self.set(model, property_name, filtered_value)

    def filter_entities(self, model, context=None):
        """
        Filter entities
        Runs filters on entity properties changing them in place.
        :param model:  object or dict
        :param context: object, dict or None
        :return: None
        """
        if model is None:
            return

        for property_name in self.entities:
            prop = self.entities[property_name]
            value = self.get(model, property_name)

            filtered_value = prop.filter(
                value=value,
                model=model,
                context=context
            )
            if value != filtered_value:  # unless changed!
                self.set(model, property_name, filtered_value)

            prop.filter_with_schema(
                model=value,
                context=context
            )

    def filter_collections(self, model, context=None):
        """
        Filter collections
        Runs filters on collection properties changing them in place.
        :param model:  object or dict
        :param context: object, dict or None
        :return: None
        """
        if model is None:
            return

        for property_name in self.collections:
            prop = self.collections[property_name]
            collection = self.get(model, property_name)
            filtered_value = prop.filter(
                value=collection,
                model=model,
                context=context
            )
            self.set(model, property_name, filtered_value)

            prop.filter_with_schema(
                collection,
                context if prop.use_context else None
            )

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
        state_result = self.validate_state(model, context=context)
        result.merge(state_result)

        # validate simple properties
        props_result = self.validate_properties(model, context=context)
        result.merge(props_result)

        # validate nested entity properties
        entities_result = self.validate_entities(model, context=context)
        result.merge(entities_result)

        # validate collection properties
        collections_result = self.validate_collections(model, context=context)
        result.merge(collections_result)

        # and return
        return result

    def validate_state(self, model, context=None):
        """
        Validate model state
        Run state validators and return and result object.
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftschema.result.Result
        """
        result = Result()
        for state_validator in self.state:
            error = state_validator.run(
                value=model,
                model=model,
                context=context
            )
            if error:
                result.add_state_errors(error)

        return result

    def validate_properties(self, model, context=None):
        """
        Validate simple properties
        Performs validation on simple properties to return a result object.
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftschema.result.Result
        """
        result = Result()
        for property_name in self.properties:
            prop = self.properties[property_name]
            value = self.get(model, property_name)
            errors = prop.validate(
                value=value,
                model=model,
                context=context
            )

            if errors:
                result.add_errors(
                    errors=errors,
                    property_name=property_name
                )

        return result

    def validate_entities(self, model, context=None):
        """
        Validate entity properties
        Performs validation on entity properties to return a result object.
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftschema.result.Result
        """
        result = Result()
        for property_name in self.entities:
            prop = self.entities[property_name]
            value = self.get(model, property_name)

            errors = prop.validate(
                value=value,
                model=model,
                context=context
            )
            if len(errors):
                result.add_entity_errors(
                    property_name=property_name,
                    direct_errors=errors
                )

            if value is None:
                continue

            schema_valid = prop.validate_with_schema(
                model=value,
                context=context
            )
            if schema_valid == False:
                result.add_entity_errors(
                    property_name,
                    schema_errors=schema_valid.errors
                )

        return result

    def validate_collections(self, model, context=None):
        """
        Validate collection properties
        Performs validation on collection properties to return a result object.
        :param model:  object or dict
        :param context: object, dict or None
        :return: shiftschema.result.Result
        """
        result = Result()
        for property_name in self.collections:
            prop = self.collections[property_name]
            collection = self.get(model, property_name)

            errors = prop.validate(
                value=collection,
                model=model,
                context=context
            )
            if len(errors):
                result.add_collection_errors(
                    property_name=property_name,
                    direct_errors=errors
                )

            collection_errors = prop.validate_with_schema(
                collection=collection,
                context=context
            )

            result.add_collection_errors(
                property_name=property_name,
                collection_errors=collection_errors
            )

        return result










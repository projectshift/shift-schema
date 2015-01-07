from pprint import pprint
from shiftvalidate.properties import Property, Entity, Collection
from shiftvalidate.exceptions import PropertyExists
from shiftvalidate.validators import AbstractValidator
from shiftvalidate.filters import AbstractFilter
from shiftvalidate.results import ValidationResult


class Schema:
    """
    Entity schema
    Contains rules for filtering and validation of an entity. Either pass in
    a definition dictionary or extend and setup object manually to use
    class-based schemas
    """

    def __init__(self, spec=None):
        """
        Initialize schema
        Configure schema by either passing a spec dictionary or
        alternatively extend from schema and implement self.schema()

        :param spec:            dict, schema specification
        :return:                None
        """

        # state validators
        self.state = []

        # property objects (each having filters and validator)
        self.properties = {}

        # linked entities
        self.entities = {}

        # linked collections
        self.collections = {}

        # init from spec
        if spec:
            self.factory(spec)

        # or create manually in subclass
        self.schema()


    def schema(self):
        """
        Schema
        This gets called at the end of construction. Implement this method
        in you class-based schemas.

        :return:                None
        """
        pass


    def factory(self, spec):
        """
        Factory method
        Instantiates itself from a spec dictionary

        :param spec:            dict
        :return:                None
        """

        # add state validators
        if 'state' in spec:
            for state_validator in spec['state']:
                self.add_state_validator(state_validator)

        # add properties
        if 'properties' in spec:
            for property in spec['properties']:
                self.add_property(property)
                for obj in spec['properties'][property]:
                    if isinstance(obj, AbstractValidator):
                        self.properties[property].add_validator(obj)
                    if isinstance(obj, AbstractFilter):
                        self.properties[property].add_filter(obj)


    def has_property(self, name):
        """
        Has property?
        A boolean method to check whether a property with the given name exists
        on schema either a simple property, linked entity or collection.

        :param name:            string, property name to check
        :return:                bool
        """
        if name in self.properties:
            return True
        if name in self.collections:
            return True
        if name in self.entities:
            return True

        # otherwise no property
        return False


    def add_state_validator(self, validator):
        """
        Add state validator
        Adds entity state validator. Those don't validate simple properties
        but instead validate an entity as whole. May be used to do
        validation across several properties (passwords match and such)

        :param validator:       shiftvalidate.validators.AbstractValidator
        :return:                None
        """
        if not isinstance(validator, AbstractValidator):
            err = '{} is not a subclass of {}'
            raise TypeError(err.format(validator, AbstractValidator))

        if not validator in self.state:
            self.state.append(validator)


    def add_property(self, name):
        """
        Add property
        Adds simple property to schema. Will raise PropertyExists if
        a property is already present.

        :param name:            string, property name
        :return:                None
        """
        if self.has_property(name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(name))
        self.properties[name] = Property()


    def add_collection(self, name):
        """
        Add collection
        Adds collection property to schema. Will raise PropertyExists if
        a property is already present.

        :param name:            string, property name
        :return:                None
        """
        if self.has_property(name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(name))
        self.collections[name] = Collection()


    def add_entity(self, name):
        """
        Add entity
        Adds linked entity property to schema. Will raise PropertyExists if
        a property is already present.

        :param name:            string, property name
        :return:                None
        """
        if self.has_property(name):
            err = 'Property "{}" already exists'
            raise PropertyExists(err.format(name))
        self.entities[name] = Entity()


    def __getattr__(self, property):
        """
        Get attribute
        Searches for an attribute in properties, linked entities and collections
        and returns the first result found.

        :param property:        a property to get
        :return:                Property, Entity or Collection
        """

        if property in self.properties.keys():
            return self.properties[property]
        if property in self.entities.keys():
            return self.entities[property]
        if property in self.collections:
            return self.collections[property]

        return object.__getattribute__(self, property)



    def process(self, model):
        """
        Process
        Accepts an entity than applies its filters and performs validation
        afterwards to return validation result object

        :param model:           object, an object to process
        :return:                shiftvalidate.results.ModelResult
        """
        self.filter(model)
        validation_result = self.validate(model)
        return validation_result


    def filter(self, model):
        """
        Filter
        Performs model property value filtering by applying through every
        attached filter. Will change model in place and return it. This
        can be used before persisting to database to ensure valid data.

        :param model:           object, an entity to filter
        :return:                object
        """

        for property in self.properties:

            # go through accessor if present
            getter = None
            if hasattr(model, 'get_' + property):
                getter = getattr(model, 'get_' + property)
            setter = None
            if hasattr(model, 'set_' + property):
                setter = getattr(model, 'set_' + property)

            # use getter
            if getter:
                value = getter(model)
            else:
                value = getattr(model, property)

            # filter
            value = self.properties[property].filter_value(
                value=value,
                context=model
            )

            # use setter
            if setter:
                setter(model, value)
            else:
                setattr(model, property, value)

            del getter, setter





    def validate(self, model):
        """
        Validate
        Perform model validation by going through all attached filters
        and validators and collect results into a result object.

        :param model:           object, an entity fo filter and validate
        :return:                shiftvalidate.results.ModelResult
        """

        result = ValidationResult()

        # validate state
        for state_validator in self.state:
            ok = state_validator.validate(value=model, context=model)
            if not ok:
                result.add_errors(property=None, errors=ok.errors)

        # validate properties
        for property in self.properties:

            # go through accessor if present
            getter = None
            if hasattr(model, 'get_' + property):
                getter = getattr(model, 'get_' + property)

            if getter:
                value = getter(model)
            else:
                value = getattr(model, property)

            ok = self.properties[property].validate_value(
                value=value,
                context=model
            )

            if not ok:
                result.add_errors(property, ok.errors)

        # done
        return result









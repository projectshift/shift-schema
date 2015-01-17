from shiftvalidate.properties import Property, Entity
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
        on schema either a simple property, linked entity.

        :param name:            string, property name to check
        :return:                bool
        """
        if name in self.properties:
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
        Searches for an attribute in properties, linked entities
        and returns the first result found.

        :param property:        a property to get
        :return:                Property, Entity
        """

        if property in self.properties.keys():
            return self.properties[property]
        if property in self.entities.keys():
            return self.entities[property]

        return object.__getattribute__(self, property)


    def get_value(self, model, property_name):
        """
        Get value
        Retrieves value from a model, possibly going through a getter
        method if it exists or directly fetching otherwise.

        :param model:           object, fetch property from it
        :param property_name:   string, property name
        :return:                mixed
        """
        if hasattr(model, 'get_' + property_name):
            getter = getattr(model, 'get_' + property_name)
            return getter()
        else:
            return getattr(model, property_name)


    def set_value(self, model, property_name, value):
        """
        Set value
        Sets value on a model, possibly going through a setter
        method if it exists or directly setting otherwise.

        :param model:           object, fetch property from it
        :param property_name:   string, property name
        :param value:           mixed, value to set
        :return:                None
        """
        if hasattr(model, 'set_' + property_name):
            setter = getattr(model, 'set_' + property_name)
            return setter(value)
        else:
            setattr(model, property_name, value)


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


    def filter(self, model, context=None):
        """
        Filter
        Performs model property value filtering by applying through every
        attached filter. Will change model in place and return it. This
        can be used before persisting to database to ensure valid data.

        :param model:           object, an entity to filter
        :return:                object
        """

        # process properties
        for property in self.properties:

            # print('FILTERING PROPERTY:', property)

            value = self.get_value(model, property)
            if value is None:
                continue

            # simple properties get model as context
            property_context = model

            # filter
            value = self.properties[property].filter_value(
                value=value,
                context=property_context
            )

            # use setter
            self.set_value(model, property, value)

        # process linked entities
        for entity_property in self.entities:

            entity = self.get_value(model, entity_property)
            if entity is None:
                continue

            # nested entities get parent entity as context
            entity_context = model

            # filter
            self.entities[entity_property].filter(
                model=entity,
                context=entity_context
            )



    def validate(self, model, context=None):
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

            # none for root, parent model for nested schemas
            state_ctx = context

            ok = state_validator.validate(value=model, context=state_ctx)
            if not ok:
                result.add_errors(property_name=None, errors=ok)

        # validate properties
        for property in self.properties:

            # go through accessor if present
            value = self.get_value(model, property)
            if value is None:
                continue

            # simple properties get model as context
            property_context = model

            # validate
            errors = self.properties[property].validate_value(
                value=value,
                context=property_context
            )

            if errors:
                result.add_errors(errors=errors, property_name=property)



        # validate linked entities
        for entity_property in self.entities:
            entity = self.get_value(model, entity_property)
            if entity is None:
                continue

            # nested entities get parent entity as context
            entity_context = model

            #validate
            ok = self.entities[entity_property].validate(
                model=entity,
                context=entity_context
            )

            if not ok:
                result.add_nested_errors(
                    property_name=entity_property,
                    errors=ok.errors
                )


        # done
        return result









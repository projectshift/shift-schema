
from shiftvalidate.properties import Property, Entity, Collection
from shiftvalidate.exceptions import PropertyExists


class Schema:
    """
    Entity schema
    Performs filtering and validation of entity property values according
    to specified rules to return a validation result object containing
    error messages (if any). Extend from this class and define your
    own filtering and validation rules for your entities.
    """

    def __init__(self, spec=None):
        """
        Initialize processor
        Configure processor by either passing a spec dictionary or
        alternatively override this method in your concrete implementations
        to define spec via setters.

        :param spec:            dict or None, processor specification
        :return:                None
        """

        # state validators
        self.state = {}

        # property objects (each having filters and validator)
        self.properties = {}

        # linked entities
        self.entities = {}

        # linked collections
        self.collections = {}

        if spec is None:
            return




    def has_property(self, name):
        """
        Has property?
        A boolean method to check whether a property with the given name exists
        on processor either a simple property, linked entity or collection.

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


    def add_property(self, name):
        """
        Add property
        Adds simple property to processor. Will raise PropertyExists if
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
        Adds collection property to processor. Will raise PropertyExists if
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
        Adds linked entity property to processor. Will raise PropertyExists if
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

        # go through each configured properties and filter onthe model

        pass


    def validate(self, model):
        """
        Validate
        Perform model validation by going through all attached filters
        and validators and collect results into a result object.

        :param model:           object, an entity fo filter and validate
        :return:                shiftvalidate.results.ModelResult
        """

        # go through each configured property and validate, collecting and
        # merging results

        pass









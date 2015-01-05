
from shiftvalidate.properties import Property, Entity, Collection
from shiftvalidate.exceptions import PropertyExists


class Processor:
    """
    Entity processor
    Performs filtering and validation of entity property values according
    to specified rules to return a validation result object containing
    error messages (if any). Extend from this class and define your
    own filtering and validation rules for your entities.
    """

    # state validators
    state_processors = {}

    # property objects (each having filters and validator)
    property_processors = {}

    # linked entity processors
    entity_processors = {}

    # collection objects
    collection_processors = {}


    def __init__(self, spec=None):
        """
        Initialize processor
        Configure processor by either passing a spec dictionary or
        alternatively override this method in your concrete implementations
        to define spec via setters.

        :param spec:            dict or None, processor specification
        :return:                None
        """
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
        if property in self.property_processors:
            return True
        if property in self.collection_processors:
            return True
        if property in self.entity_processors:
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
        self.property_processors[name] = Property()


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
        self.property_processors[name] = Collection()


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
        self.entity_processors[name] = Entity()


    def validate(self, model):
        """
        Validate
        Perform model validation by going through all attached filters
        and validators and collect results into a result object.

        :param model:           object, an entity fo filter and validate
        :return:                shiftvalidate.results.ModelResult
        """
        pass


    def filter(self, model):
        """
        Filter
        Performs model property value filtering by applying through every
        attached filter. Will change model in place and return it. This
        can be used before persisting to database to ensure valid data.

        :param model:           object, an entity to filter
        :return:                object
        """
        pass


    def process(self, model):
        """
        Process
        Accepts an entity than applies its filters and performs validation
        afterwards to return validation result object

        :param model:           object, an object to process
        :return:                shiftvalidate.results.ModelResult
        """
        pass



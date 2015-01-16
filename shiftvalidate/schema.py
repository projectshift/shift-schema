
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
        Factory method
        Configures itself from a spec dictionary

        :param spec: dict
        :return: None
        """


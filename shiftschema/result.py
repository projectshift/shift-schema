from pprint import pformat
from copy import deepcopy
from shiftschema import exceptions as x


class Error:
    """
    Error
    Represents a single validation check result that evaluates to bool to
    indicate whether the result is valid. In case it's not wil hold the
    error message and optional kwargs for parametrized translation.
    """
    def __init__(self, message=None, kwargs=None):
        """
        Initialize
        Accepts error message and optional iterable of parameters used to
        format at translation time.

        :param message:             str or None
        :param kwargs:              iterable or None
        :return:                    None
        """
        self.message = message
        self.kwargs = kwargs

    def __bool__(self):
        return self.message is not None

    def __repr__(self):
        r = '<{} object message="{}">'
        return r.format(self.__class__.__qualname__, self.message)


class Result:
    """
    Result
    Represents result of validating with a schema. Contains properties and
    their errors but can also contain nested results for nested schemas.
    """
    def __init__(self, errors=None, translator=None, locale='en'):
        if not errors:
            errors = dict()
        self.errors = errors
        self.translator = translator
        self.locale=locale

    def __bool__(self):
        # todo: check for collection errors to evaluate
        return not self.errors

    def __eq__(self, other):
        return self.__bool__() == other

    def __ne__(self, other):
        return self.__bool__() != other

    def __repr__(self):
        return pformat(self.errors)

    def add_state_errors(self, errors):
        """
        Add state errors
        Accepts a list of errors (or a single Error) coming from validators
        applied to entity as whole that are used for entity state validation
        The errors will exist on a  __state__ property of the errors object.

        :param errors: list or Error, list of entity state validation errors
        :return: shiftschema.result.Result
        """
        if not self.errors:
            self.errors = dict()
        if '__state__' not in self.errors:
            self.errors['__state__'] = []

        if type(errors) is not list:
            errors = [errors]
        for error in errors:
            if not isinstance(error, Error):
                err = 'Error must be of type {}'
                raise x.InvalidErrorType(err.format(Error))

            self.errors['__state__'].append(error)

        return self

    def add_errors(self, property_name, errors):
        """
        Add one or several errors to properties.
        :param property_name: str, property name
        :param errors: list or Error, error object(s)
        :return: shiftschema.result.Result
        """
        if type(errors) is not list:
            errors = [errors]
        for error in errors:
            if not isinstance(error, Error):
                err = 'Error must be of type {}'
                raise x.InvalidErrorType(err.format(Error))

        if property_name in self.errors:
            self.errors[property_name].extend(errors)
        else:
            self.errors[property_name] = errors

        return self

    def add_entity_errors(
        self,
        property_name,
        direct_errors=None,
        schema_errors=None
    ):
        """
        Attach nested entity errors
        Accepts a list errors coming from validators attached directly,
        or a dict of errors produced by a nested schema.

        :param property_name: str, property name
        :param direct_errors: list, errors from validators attached directly
        :param schema_errors: dict, errors from nested schema
        :return: shiftschema.result.Result
        """
        if direct_errors is None and schema_errors is None:
            return self

        # direct errors
        if direct_errors is not None:
            if property_name not in self.errors:
                self.errors[property_name] = dict()

            if 'direct' not in self.errors[property_name]:
                self.errors[property_name]['direct'] = []

            if type(direct_errors) is not list:
                direct_errors = [direct_errors]

            for error in direct_errors:
                if not isinstance(error, Error):
                    err = 'Error must be of type {}'
                    raise x.InvalidErrorType(err.format(Error))
                self.errors[property_name]['direct'].append(error)

        # schema errors
        if schema_errors is not None:
            if isinstance(schema_errors, Result):
                schema_errors = schema_errors.errors

            if not schema_errors:
                return self

            if property_name not in self.errors:
                self.errors[property_name] = dict()

            if 'schema' not in self.errors[property_name]:
                self.errors[property_name]['schema'] = schema_errors
            else:
                self.errors[property_name]['schema'] = self.merge_errors(
                    self.errors[property_name]['schema'],
                    schema_errors
                )

        return self

    def add_collection_errors(
        self,
        property_name,
        direct_errors=None,
        collection_errors=None
    ):
        """
        Add collection errors
        Accepts a list errors coming from validators attached directly,
        or a list of schema results for each item in the collection.

        :param property_name: str, property name
        :param direct_errors: list, errors from validators attached directly
        :param collection_errors: list, list of errors for collection members
        :return: shiftschema.result.Result
        """
        if direct_errors is None and collection_errors is None:
            return self

        # direct errors
        if direct_errors is not None:
            if type(direct_errors) is not list:
                direct_errors = [direct_errors]
            if property_name not in self.errors:
                self.errors[property_name] = dict()
            if 'direct' not in self.errors[property_name]:
                self.errors[property_name]['direct'] = []
            for error in direct_errors:
                if not isinstance(error, Error):
                    err = 'Error must be of type {}'
                    raise x.InvalidErrorType(err.format(Error))
                self.errors[property_name]['direct'].append(error)

        # collection errors
        if collection_errors:
            enum = enumerate(collection_errors)
            errors_dict = {i: e for i, e in enum if not bool(e)}
            if not errors_dict:
                return self

            if property_name not in self.errors:
                self.errors[property_name] = dict()
            if 'collection' not in self.errors[property_name]:
                self.errors[property_name]['collection'] = errors_dict
            else:
                self.errors[property_name]['collection'] = self.merge_errors(
                    self.errors[property_name]['collection'],
                    errors_dict
                )

        return self

    def merge_errors(self, errors_local, errors_remote):
        """
        Merge errors
        Recursively traverses error graph to merge remote errors into local
        errors to return a new joined graph.

        :param errors_local: dict, local errors, will be updated
        :param errors_remote: dict, remote errors, provides updates
        :return: dict
        """
        for prop in errors_remote:

            # create if doesn't exist
            if prop not in errors_local:
                errors_local[prop] = errors_remote[prop]
                continue

            local = errors_local[prop]
            remote = errors_remote[prop]

            # check compatibility
            if not isinstance(local, type(remote)):
                msg = 'Type mismatch on property [{}] when merging errors. '
                msg += 'Unable to merge [{}] into [{}]'
                raise x.UnableToMergeResultsType(msg.format(
                    prop,
                    type(errors_remote[prop]),
                    type(self.errors[prop])
                ))

            mismatch = 'Unable to merge nested entity errors with nested '
            mismatch += 'collection errors on property [{}]'
            if 'schema' in local and 'collection' in remote:
                raise x.UnableToMergeResultsType(mismatch.format(prop))
            if 'collection' in local and 'schema' in remote:
                raise x.UnableToMergeResultsType(mismatch.format(prop))

            # merge simple & state
            if type(remote) is list:
                errors_local[prop].extend(remote)
                continue

            # merge direct errors on nested entities and collection
            if 'direct' in remote and 'direct' not in local:
                errors_local[prop]['direct'] = remote['direct']
            if 'direct' in remote and 'direct' in local:
                errors_local[prop]['direct'].extend(remote['direct'])

            # merge nested schema errors
            if 'schema' in remote and not 'schema' in local:
                errors_local[prop]['schema'] = remote['schema']
            if 'schema' in remote and 'schema' in local:
                errors_local[prop]['schema'] = self.merge_errors(
                    errors_local[prop]['schema'],
                    remote['schema']
                )

            # todo: merge nested collection
            # merge nested collections errors

        # and return
        return errors_local

    def merge(self, another):
        """ Merges another validation result graph into itself"""
        if isinstance(another, Result):
            another = another.errors
        self.errors = self.merge_errors(self.errors, another)

    def get_messages(self, locale=None):
        """ Get a dictionary of translated messages """
        if locale is None:
            locale = self.locale

        if self.translator:
            def translate(error):
                return self.translator.translate(error, locale)
        else:
            def translate(error):
                return error

        errors = deepcopy(self.errors)
        errors = self._translate_errors(errors, translate)
        return errors

    # todo: refactor to work with entity and collection errors
    def _translate_errors(self, errors, translate):
        """ Recursively apply translate callback to each error message"""
        for property_name in errors:
            property_errors = errors[property_name]
            if type(property_errors) is list:
                for index,error in enumerate(property_errors):
                    message = translate(error.message)
                    message = self.format_error(message, error.kwargs)
                    errors[property_name][index] = message
            elif type(property_errors) is dict:
                errors[property_name] = self._translate_errors(
                    property_errors,
                    translate
                )

        return errors

    def format_error(self, error, args=None):
        """ Format error with positional or named arguments (if any) """
        if type(args) is dict:
            return error.format(**args)
        if type(args) is list or type(args) is tuple:
            return error.format(*args)

        return error







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

    def __eq__(self, other):
        return self.__bool__() == other

    def __ne__(self, other):
        return self.__bool__() != other

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

        if property_name not in self.errors:
            self.errors[property_name] = dict()

        # direct errors
        if direct_errors is not None:
            if '__direct__' not in self.errors[property_name]:
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
            if 'schema' not in self.errors[property_name]:
                self.errors[property_name]['schema'] = dict()

            if isinstance(schema_errors, Result):
                schema_errors = schema_errors.errors

            self.errors[property_name]['schema'] = schema_errors

        return self







    def add_collection_errors(self):
        pass

    def merge2(self, another):
        if isinstance(another, Result):
            another = another.errors

        for prop in another:

            # create if doesn't exist
            if prop not in self.errors:
                self.errors[prop] = another[prop]
                continue

            local = self.errors[prop]
            remote = another[prop]

            # check compatibility
            if not isinstance(local, type(remote)):
                msg = 'Type mismatch on property [] when merging errors.'
                msg += 'Unable to merge [{}] into [{}]'
                raise x.UnableToMergeResultsType(msg.format(
                    prop,
                    type(another[prop]),
                    type(self.errors[prop])
                ))

            for what in ['schema', 'collection']:
                if what in local and what not in remote:
                    msg = 'Unable to merge nested entity errors with nested '
                    msg += 'collection errors on property [{}]'
                    raise x.UnableToMergeResultsType(msg.format(prop))

            # merge simple
            if type(remote) is list:
                self.errors[prop].extend(remote)




        print()
        print('MERGING:')
        print(self)




    # todo: refactor to support entity and collection errors
    def merge(self, another):
        """ Merge another result into itself """
        if not isinstance(another, Result):
            err = 'Unable to merge: must be "{}", got "{}"'
            raise x.InvalidResultType(err.format(Result, another))

        errors = another.errors
        for property_name in errors:
            if property_name in self.errors:
                self.errors[property_name].extend(errors[property_name])
            else:
                self.errors[property_name] = errors[property_name]
                
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







from abc import ABCMeta, abstractmethod
from shiftschema.result import Error
from shiftschema.exceptions import InvalidErrorType


class AbstractValidator(metaclass=ABCMeta):
    """
    Abstract validator
    Provides a base for concrete validators and your custom validators. All
    of those can be added to simple properties on the processor.
    """

    @abstractmethod
    def validate(self, value, context=None):
        """
        Validate
        Abstract validation method: implement this in your concrete
        validators. Performs validation of provided value optionally with
        context (object being validated) and returns a result Error object
        that evaluates to boolean.

        :param value:               a value to validate
        :param context:             validation context
        :return:                    shiftschema.result.Error
        """
        return

    def run(self, value, context=None):
        """
        Run validation
        Wraps concrete implementation to ensure custom validators return
        proper type of result.

        :param value:               a value to validate
        :param context:             validation context
        :return:                    shiftschema.result.Error
        """
        res = self.validate(value, context)
        if not isinstance(res, Error):
            err = 'Validator "{}" result must be of type "{}", got "{}"'
            raise InvalidErrorType(err.format(
                self.__class__.__name__,
                Error,
                type(res))
            )

        return res

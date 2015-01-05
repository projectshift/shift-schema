from abc import ABCMeta, abstractmethod

class AbstractValidator(metaclass=ABCMeta):

    @abstractmethod
    def validate(self, value, context=None):
        """
        Validate
        Abstract validation method: implement this in your concrete
        validators. Performs validation of provided value optionally with
        context (object being validated) and returns a result that if
        either boolean true, or a string representing error message.

        :param value:               a value to validate
        :param context:             validation context
        :return:                    True or string error
        """
        return


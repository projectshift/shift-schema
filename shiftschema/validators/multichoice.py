from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
from shiftschema.exceptions import InvalidOption


class MultiChoice(AbstractValidator):
    """
    MultiChoice validator
    Accepts a list of values and checks if every item is a valid choice.
    """

    invalid_multichoice = '%invalid_multichoice%'

    def __init__(self, valid_choices=None, message=None):
        """
        Initialize validator
        Accepts an iterable of valid choices to check against.

        :param min:             int or None, minimum length
        :param max:             int or None, maximum length
        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.invalid_multichoice = message

        try:
            iter(valid_choices)
        except TypeError:
            raise InvalidOption('Choices must be an iterable')

        self.choices = valid_choices

    def validate(self, value, context=None):
        """
        Validate
        Perform value validation against validation settings and return
        error object.

        :param value:           list, value to check
        :param context:         object or None, validation context
        :return:                shiftschema.result.Error
        """
        invalid = [item for item in value if item not in self.choices]
        if len(invalid):
            return Error(
                self.invalid_multichoice,
                dict(items=', '.join(invalid))
            )

        # success otherwise
        return Error()




from shiftschema.validators import AbstractValidator, Length, Choice
from shiftschema.filters import AbstractFilter, Strip, Digits
from shiftschema.result import Error
from shiftschema.schema import Schema

# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------


class ValidatorValid(AbstractValidator):
    """ Test validator that is always valid"""
    def validate(self, value=None, context=None):
        return Error() # always valid


class ValidatorInvalid(AbstractValidator):
    """ Test validator that is always invalid"""
    def validate(self, value=None, context=None):
        return Error('always invalid')


class EntityFilter(AbstractFilter):
    """ A simple filter that can be used on entity properties """
    def filter(self, value, context=None):
        return [value]


# simple person spec
person_spec = {
    'state': [ValidatorValid()],
    'properties': {
        'first_name': dict(
            filters=[Strip()],
            validators=[Length(min=2, max=10)],
        ),
        'last_name': dict(
            filters=[Strip()],
            validators=[Length(min=2, max=10)],
        ),
        'salutation': dict(
            filters=[Strip()],
            validators=[Choice(['mr', 'ms'])]
        ),
        'birth_year': dict(
            filters=[Strip(), Digits(to_int=True)]
        ),
    },
}

# aggregate person spec (contains nested schema)
person_spec_aggregate = {
    'state': [ValidatorValid()],
    'properties': {
        'first_name': dict(
            filters=[Strip()],
            validators=[Length(min=2, max=10)],
        ),
        'last_name': dict(
            filters=[Strip()],
            validators=[Length(min=2, max=10)],
        ),
        'salutation': dict(
            filters=[Strip()],
            validators=[Choice(['mr', 'ms'])]
        ),
        'birth_year': dict(
            filters=[Strip(), Digits(to_int=True)]
        ),
    },
    'entities': {
        'spouse': dict(
            required=True,
            required_message='XXX',
            schema=Schema(person_spec)
        )
    }
}


class Person:
    """
    Person
    Represents as entity being tested
    """
    def __init__(
        self,
        first_name=None,
        last_name=None,
        email=None,
        salutation=None,
        birth_year=None
    ):
        self.id = 123
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.salutation = salutation
        self.birth_year = birth_year

    def __repr__(self):
        r = '<Person first=[{}] last=[{}] email=[{}] salutation=[{}] year=[{}]>'
        return r.format(
            self.first_name,
            self.last_name,
            self.email,
            self.salutation,
            self.birth_year
        )
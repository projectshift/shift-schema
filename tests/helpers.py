
from shiftvalidate.validators import AbstractValidator, Length, Choice
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.result import Error
from shiftvalidate.schema import Schema

# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------

class StateValidator(AbstractValidator):
    def validate(self, value=None, context=None):
        return Error() # always valid

class StateValidatorInvalid(AbstractValidator):
    def validate(self, value=None, context=None):
        return Error('always invalid') # always invalid

# simple person spec
person_spec = {
    'state': [StateValidator()],
    'properties': {
        'first_name': [
            '__required__',
            Strip(),
            Length(min=2, max=10)
        ],
        'last_name': [
            '__required__',
            Strip(),
            Length(min=2, max=10)
        ],
        'salutation': [
            Strip(),
            Choice(['mr', 'ms'])
        ],
        'birth_year': [
            Strip(),
            Digits(to_int=True)
        ]
    }
}

# aggregate person spec (contains nested schema)
person_spec_aggregate = {
    'state': [StateValidator()],
    'properties': {
        'first_name': [
            '__required__',
            Strip(),
            Length(min=1, max=10)
        ],
        'last_name': [
            '__required__',
            Strip(),
            Length(min=1, max=10)
        ],
        'salutation': [
            Strip(),
            Choice(['mr', 'ms'])
        ],
        'birth_year': [
            Strip(),
            Digits(to_int=True)
        ],
        'spouse': [
            '__required__',
            Schema(person_spec)
        ]
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
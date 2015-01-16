
from shiftvalidate.validators import AbstractValidator, Length, Choice
from shiftvalidate.filters import Strip, Digits
from shiftvalidate.result import Error

# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------

class StateValidator(AbstractValidator):
    def validate(self, value=None, context=None):
        return Error() # always valid

person_spec = {
    'state': [StateValidator()],
    'properties': {
        'first_name': [
            Strip(),
            Length(min=1, max=10)
        ],
        'last_name': [
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
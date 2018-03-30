
from shiftschema import validators
from shiftschema import filters
from shiftschema.result import Error
from shiftschema.schema import Schema

# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------


class ValidatorValid(validators.AbstractValidator):
    """ Test validator that is always valid"""
    def validate(self, value=None, context=None):
        return Error() # always valid


class ValidatorInvalid(validators.AbstractValidator):
    """ Test validator that is always invalid"""
    def validate(self, value=None, context=None):
        return Error('always invalid')


class EntityFilter(filters.AbstractFilter):
    """ A simple filter that can be used on entity properties """
    def filter(self, value, context=None):
        return [value]


class CollectionFilter(filters.AbstractFilter):
    """ Test filter to apply to collection properties """
    def filter(self, value, context=None):
        filtered = filter(lambda x: x['value'] % 2 == 0, value)
        return list(filtered)


class DropUSAddressesCollectionFilter(filters.AbstractFilter):
    """ Goes through a collection of addresses and drops US ones """
    def filter(self, value, context=None):
        return [a for a in value if a.country.strip() != 'US']


# simple person spec
person_spec = {
    'state': [ValidatorValid()],
    'properties': {
        'first_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'last_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'salutation': dict(
            filters=[filters.Strip()],
            validators=[validators.Choice(['mr', 'ms'])]
        ),
        'birth_year': dict(
            filters=[filters.Strip(), filters.Digits(to_int=True)]
        ),
    },
}

# address spec
address_spec = {
    'properties': {
        'address': dict(
            filters=[filters.Strip()],
            validators=[validators.Required()],
        ),
        'city': dict(
            filters=[filters.Strip()],
            validators=[validators.Required()],
        ),
        'country': dict(
            filters=[filters.Strip()],
            validators=[validators.Required()],
        ),
        'postcode': dict(
            filters=[filters.Strip()],
            validators=[validators.Required()],
        )
    }
}

# aggregate person spec (contains nested schema)
person_spec_aggregate = {
    'state': [ValidatorValid()],
    'properties': {
        'first_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'last_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'salutation': dict(
            filters=[filters.Strip()],
            validators=[validators.Choice(['mr', 'ms'])]
        ),
        'birth_year': dict(
            filters=[filters.Strip(), filters.Digits(to_int=True)]
        ),
    },
    'entities': {
        'spouse': dict(
            validators=[validators.Required()],
            schema=Schema(person_spec)
        )
    },
    'collections': {
        'addresses': dict(
            filters=[DropUSAddressesCollectionFilter()],
            validators=[validators.NotEmpty()],
            schema=Schema(address_spec)
        )
    }
}

# aggregate person spec (contains nested collection)
person_spec_collection_aggregate = {
    'state': [ValidatorValid()],
    'properties': {
        'first_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'last_name': dict(
            filters=[filters.Strip()],
            validators=[validators.Length(min=2, max=10)],
        ),
        'salutation': dict(
            filters=[filters.Strip()],
            validators=[validators.Choice(['mr', 'ms'])]
        ),
        'birth_year': dict(
            filters=[filters.Strip(), filters.Digits(to_int=True)]
        ),
    },
    'collections': {
        'addresses': dict(
            filters=[DropUSAddressesCollectionFilter()],
            validators=[validators.NotEmpty()],
            schema=Schema(address_spec)
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
        self.spouse = None
        self.addresses = []

    def __repr__(self):
        r = '<Person first=[{}] last=[{}] email=[{}] salutation=[{}] year=[{}]>'
        return r.format(
            self.first_name,
            self.last_name,
            self.email,
            self.salutation,
            self.birth_year
        )


class Address:
    """
    Address
    Represents an address entity that can be attached to a person on its
    addresses collection property
    """
    def __init__(
        self,
        address=None,
        city=None,
        country=None,
        postcode=None,
    ):
        self.id = 456
        self.address = address
        self.city = city
        self.country = country
        self.postcode = postcode

    def __repr__(self):
        r = '<Address address=[{}] city=[{}] country=[{}] postcode=[{}]>'
        return r.format(
            self.address,
            self.city,
            self.country,
            self.postcode
        )

from shiftschema import validators
from shiftschema import filters
from shiftschema.result import Error
from shiftschema.schema import Schema

# -----------------------------------------------------------------------------
# Test helpers
# -----------------------------------------------------------------------------


class ValidatorValid(validators.AbstractValidator):
    """ Test validator that is always valid"""
    def validate(self, value=None, model=None, context=None):
        return Error() # always valid


class ValidatorInvalid(validators.AbstractValidator):
    """ Test validator that is always invalid"""
    def validate(self, value=None, model=None, context=None):
        return Error('always invalid')


class EntityFilter(filters.AbstractFilter):
    """ A simple filter that can be used on entity properties """
    def filter(self, value, model=None, context=None):
        return [value]


class CollectionFilter(filters.AbstractFilter):
    """ Test filter to apply to collection properties """
    def filter(self, value, model=None, context=None):
        filtered = filter(lambda x: x['value'] % 2 == 0, value)
        return list(filtered)


class DropUSAddressesCollectionFilter(filters.AbstractFilter):
    """ Goes through a collection of addresses and drops US ones """
    def filter(self, value, model=None, context=None):
        return [a for a in value if a.country.strip() != 'US']


# simple person spec
class PersonSpec(Schema):
    def schema(self):

        self.add_state_validator(ValidatorValid())

        self.add_property('first_name')
        self.first_name.add_filter(filters.Strip())
        self.first_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('last_name')
        self.last_name.add_filter(filters.Strip())
        self.last_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('salutation')
        self.salutation.add_filter(filters.Strip())
        self.salutation.add_validator(validators.Choice(['mr', 'ms']))

        self.add_property('birth_year')
        self.birth_year.add_filter(filters.Strip())
        self.birth_year.add_filter(filters.Digits(to_int=True))


# address spec
class AddressSpec(Schema):
    def schema(self):
        self.add_property('address')
        self.address.add_filter(filters.Strip())
        self.address.add_validator(validators.Required())

        self.add_property('city')
        self.city.add_filter(filters.Strip())
        self.city.add_validator(validators.Required())

        self.add_property('country')
        self.country.add_filter(filters.Strip())
        self.country.add_validator(validators.Required())

        self.add_property('postcode')
        self.postcode.add_filter(filters.Strip())
        self.postcode.add_validator(validators.Required())


# aggregate person spec (contains nested schema)
class PersonSpecAggregate(Schema):
    def schema(self):

        self.add_state_validator(ValidatorValid())

        self.add_property('first_name')
        self.first_name.add_filter(filters.Strip())
        self.first_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('last_name')
        self.last_name.add_filter(filters.Strip())
        self.last_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('salutation')
        self.salutation.add_filter(filters.Strip())
        self.salutation.add_validator(validators.Choice(['mr', 'ms']))

        self.add_property('birth_year')
        self.birth_year.add_filter(filters.Strip())
        self.birth_year.add_filter(filters.Digits(to_int=True))

        self.add_entity('spouse')
        self.spouse.add_validator(validators.Required())
        self.spouse.schema = PersonSpec()

        self.add_collection('addresses')
        self.addresses.schema = AddressSpec()
        self.addresses.add_filter(DropUSAddressesCollectionFilter())
        self.addresses.add_validator(validators.NotEmpty())


# aggregate person spec (contains nested collection)
class PersonSpecCollectionAggregate(Schema):
    def schema(self):

        self.add_state_validator(ValidatorValid())

        self.add_property('first_name')
        self.first_name.add_filter(filters.Strip())
        self.first_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('last_name')
        self.last_name.add_filter(filters.Strip())
        self.last_name.add_validator(validators.Length(min=2, max=10))

        self.add_property('salutation')
        self.salutation.add_filter(filters.Strip())
        self.salutation.add_validator(validators.Choice(['mr', 'ms']))

        self.add_property('birth_year')
        self.birth_year.add_filter(filters.Strip())
        self.birth_year.add_filter(filters.Digits(to_int=True))

        self.add_collection('addresses')
        self.addresses.schema = AddressSpec()
        self.addresses.add_filter(DropUSAddressesCollectionFilter())
        self.addresses.add_validator(validators.NotEmpty())


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
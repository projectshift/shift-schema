from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.translator import Translator
from shiftschema.result import Result,Error
from shiftschema import validators as validator

@attr('translations', 'messages')
class MessageTranslationsTests(TestCase):

    locale = 'en'

    def validate_messages(self, expected, actual):
        """ A helper to check messages """
        for exp in expected:
            error = 'Expected message [{}] not found.'.format(exp)
            self.assertTrue(exp in actual, msg=error)

    def result(self):
        """ Preconfigured result object """
        result = Result(translator=Translator(), locale=self.locale)
        return result


    def test_translatable_digits(self):
        """ Digits validator is translatable """
        result = self.result()
        errors = [Error(validator.Digits.not_digital)]

        result.add_errors(errors, 'property')
        msgs = result.get_messages()

        exp = ['Must only consist of digits.']
        self.validate_messages(exp, msgs['property'])

    def test_translatable_choice(self):
        """ Choice validator is translatable """
        result = self.result()
        errors = [Error(validator.Choice.invalid_choice)]

        result.add_errors(errors, 'property')
        msgs = result.get_messages(locale='en')

        exp = ['Provided value is not a valid choice']
        self.validate_messages(exp, msgs['property'])

    def test_translatable_length(self):
        """ Length validator is translatable """
        result = self.result()
        params = dict(min=10,max=100)
        errors = [
            Error(validator.Length.too_long, params),
            Error(validator.Length.too_short, params),
            Error(validator.Length.not_in_range, params),
        ]

        result.add_errors(errors, 'property')
        msgs = result.get_messages(locale='en')

        exp = [
            'String is too long. Maximum is 100',
            'String is too short. Minimum is 10',
            'String length not in range 10-100 characters'
        ]
        self.validate_messages(exp, msgs['property'])

    def test_translatable_email(self):
        """ Length validator is translatable """
        result = self.result()
        params = dict()
        errors = [
            Error(validator.Email.not_email, params),
        ]

        result.add_errors(errors, 'property')
        msgs = result.get_messages(locale='en')

        exp = [
            'This is not a valid email',
        ]
        self.validate_messages(exp, msgs['property'])
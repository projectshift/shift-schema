from unittest import TestCase
from shiftschema.validators import Email


class EmailValidatorTest(TestCase):
    """ Email validator test"""

    def test_create(self):
        """ Can instantiate email validator """
        validator = Email(message='Custom error')
        self.assertIsInstance(validator, Email)

    def test_valid_email_passes(self):
        """ Valid email passes checks """
        validator = Email()
        error = validator.validate('myself@icloud.com')
        self.assertFalse(error)

    def test_invalid_email_fails(self):
        """ Invalid email fails """
        validator = Email()
        error = validator.validate('not-an-email')
        self.assertTrue(error)
        self.assertTrue(type(error.message) is str)

    def test_various_emails(self):
        """ Validating various emails """
        validator = Email()

        valid = [
            'something@local',
            'cal@iamcalx.com',
            'cal+henderson@iamcalx.com',
            '"cal henderson"@iamcalx.com',
            'cal@iamcalx',
            'cal@[hello world].com',
            'abcdefghijklmnopqrstuvwxyz@abcdefghijklmnopqrstuvwxyz'
        ]

        for address in valid:
            error = validator.validate(address)
            msg = 'Email [{}] failed validation'.format(address)
            self.assertFalse(error, msg=msg)


        invalid = [
            'cal@iamcalx com',
            'cal henderson@iamcalx.com',
            'cal@hello world.com',
        ]

        for address in invalid:
            error = validator.validate(address)
            msg = 'Email [{}] failed validation'.format(address)
            self.assertTrue(error, msg=msg)



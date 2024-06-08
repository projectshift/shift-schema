from unittest import TestCase
from shiftschema.validators import Ip


class IpValidatorTest(TestCase):

    def test_create(self):
        """ Can instantiate IP validator """
        validator = Ip()
        self.assertIsInstance(validator, Ip)

    def test_valid_ip_v4_passes_validation(self):
        """ Valid IPv4 address passes validation"""
        ip = '217.150.99.254'
        validator = Ip()
        error = validator.validate(ip)
        self.assertFalse(error)

    def test_valid_ip_v6_passes_validation(self):
        """ Valid IPv6 passes validation """
        ip = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        validator = Ip()
        error = validator.validate(ip)
        self.assertFalse(error)

    def test_invalid_ip_fails_validation(self):
        """ Invalid IP fails validation"""
        ip = 'not an ip'
        validator = Ip(message='Bad ip')
        error = validator.validate(ip)
        self.assertTrue(error)



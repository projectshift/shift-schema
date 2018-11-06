from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.validators import Url

# these are valid urls
valid = [
    "http://foo.com/blah_blah",
    "http://foo.com/blah_blah/",
    "http://foo.com/blah_blah_(wikipedia)",
    "http://foo.com/blah_blah_(wikipedia)_(again)",
    "http://www.example.com/wpstyle/?p=364",
    "https://www.example.com/foo/?bar=baz&inga=42&quux",
    "http://✪df.ws/123",
    "http://userid:password@example.com:8080",
    "http://userid:password@example.com:8080/",
    "http://userid@example.com",
    "http://userid@example.com/",
    "http://userid@example.com:8080",
    "http://userid@example.com:8080/",
    "http://userid:password@example.com",
    "http://userid:password@example.com/",
    "http://142.42.1.1/",
    "http://142.42.1.1:8080/",
    "http://➡.ws/䨹",
    "http://⌘.ws",
    "http://⌘.ws/",
    "http://foo.com/blah_(wikipedia)#cite-1",
    "http://foo.com/blah_(wikipedia)_blah#cite-1",
    "http://foo.com/unicode_(✪)_in_parens",
    "http://foo.com/(something)?after=parens",
    "http://☺.damowmow.com/",
    "http://code.google.com/events/#&product=browser",
    "http://j.mp",
    "ftp://foo.bar/baz",
    "http://foo.bar/?q=Test%20URL-encoded%20stuff",
    "http://مثال.إختبار",
    "http://例子.测试",
    "http://उदाहरण.परीक्षा",
    "http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
    "http://1337.net",
    "http://a.b-c.de",
    "http://223.255.255.254",
    "https://foo_bar.example.com/",
]

# these are invalid urls
invalid = [
    "http://",
    "http://.",
    "http://..",
    "http://../",
    "http://?",
    "http://??",
    "http://??/",
    "http://#",
    "http://##",
    "http://##/",
    "http://foo.bar?q=Spaces should be encoded",
    "//",
    "//a",
    "///a",
    "///",
    "http:///a",
    "foo.com",
    "rdar://1234",
    "h://test",
    "http:// shouldfail.com",
    ":// should fail",
    "http://foo.bar/foo(bar)baz quux",
    "ftps://foo.bar/",
    "http://-error-.invalid/",
    "http://a.b--c.de/",
    "http://-a.b.co",
    "http://a.b-.co",
    "http://0.0.0.0",
    "http://10.1.1.0",
    "http://10.1.1.255",
    "http://224.1.1.1",
    "http://1.1.1.1.1",
    "http://123.123.123",
    "http://3628126748",
    "http://.www.foo.bar/",
    "http://www.foo.bar./",
    "http://.www.foo.bar./",
    "http://10.1.1.1",
    "http://10.1.1.254",
]



@attr('validator', 'url')
class UrlTest(TestCase):

    def test_create(self):
        """ Can instantiate URL validator """
        validator = Url()
        self.assertIsInstance(validator, Url)

    # def test_can_fail(self):
    #     """ Validating digits and failing """
    #     value = '123r456'
    #     validator = Digits()
    #     error = validator.validate(value)
    #     self.assertTrue(error)
    #     self.assertTrue(type(error.message) is str)
    #
    #
    # def test_can_fail_with_custom_message(self):
    #     """ Digits validator accepts custom error """
    #     msg = 'Me is custom error'
    #     validator = Digits(msg)
    #     error = validator.validate('123r456')
    #     self.assertEqual(msg, error.message)
    #
    #
    # def test_can_pass(self):
    #     """ Valid digits input passes validation  """
    #
    #     validator = Digits()
    #     error1 = validator.validate('123456')
    #     error2 = validator.validate(123456)
    #
    #     self.assertFalse(error1)
    #     self.assertFalse(error2)


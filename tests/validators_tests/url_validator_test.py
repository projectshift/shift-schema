from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.validators import Url
import re

# these are valid urls
valid = [
    "http://foo.com/blah_blah",
    "//foo.com/blah_blah",
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
    "https://папироска.рф"
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

    def test_valid_urls_pass(self):
        """ Valid urls pass validation """
        validator = Url(protocols=['http', 'https', 'ftp', 'sftp'])
        for url in valid:
            error = validator.validate(url)
            if error:
                err = 'Valid url [{}] failed validation'
                self.fail(err.format(url))

    def test_invalid_urls_fail(self):
        """ Invalid urls fail validation """
        validator = Url(protocols=['http', 'https', 'ftp', 'sftp'])
        for url in invalid:
            error = validator.validate(url)
            if not error:
                err = 'Invalid url [{}] passed validation'
                self.fail(err.format(url))

    def test_can_use_localhost(self):
        """ Can allow localhost in URLs"""
        validator = Url(localhost=True)
        url = 'http://localhost:5000'
        error = validator.validate(url)
        if error:
            self.fail('URL [{}] failed'.format(url))



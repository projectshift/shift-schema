from unittest import TestCase
from nose.plugins.attrib import attr

@attr('translator')
class ErrorTest(TestCase):
    pass

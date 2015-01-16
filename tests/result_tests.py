from unittest import TestCase
from nose.plugins.attrib import attr

from shiftvalidate.result import Error, Result

@attr('result', 'error')
class ErrorTest(TestCase):

    def test_create_error(self):
        """ Creating an error object """
        err = Error('message')
        self.assertIsInstance(err, Error)

    def test_error_evaluates_to_true(self):
        """ Error with a message evaluates to true"""
        err = Error('message')
        self.assertTrue(err)
        self.assertTrue(err == True)
        self.assertTrue(err != False)

    def test_empty_error_evaluates_to_false(self):
        """ Empty error object evaluates to false """
        err = Error()
        self.assertFalse(err)
        self.assertFalse(err == True)
        self.assertFalse(err != False)

@attr('result', 'result')
class ResultTest(TestCase):
    def test_create_error(self):
        """ Creating result object """
        msgs = {'what?': 'error'}
        result = Result(msgs)
        self.assertIsInstance(result, Result)
        self.assertEquals(msgs, result.errors)
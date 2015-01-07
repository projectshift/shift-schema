from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.results import SimpleResult

@attr('simple_result')
class SimpleResultTests(TestCase):
    """
    Example test
    This is an example to demonstrate unittests are working
    """

    def test_create_simple_result(self):
        """ Can create simple result """
        res = SimpleResult()
        self.assertIsInstance(res, SimpleResult)


    def test_simple_result_failure_evaluates_to_false(self):
        """ Falsy result evaluates to boolean false """
        res = SimpleResult(errors='error')

        self.assertFalse(res)
        self.assertTrue(not res)
        self.assertTrue(res == False)
        self.assertTrue(res != True)
        self.assertTrue(bool(res) is False)


    def test_simple_result_succes_evaluates_to_true(self):
        """ Truthy result evaluates to  boolean true"""
        res = SimpleResult()

        self.assertTrue(res)
        self.assertTrue(res == True)
        self.assertTrue(res != False)
        self.assertTrue(bool(res) is True)

    def test_set_single_error(self):
        """ Can set single error on result """
        error = 'Me is error message'
        res = SimpleResult(error)
        self.assertTrue(type(res.errors) is list)
        self.assertTrue(error in res.errors)


    def test_set_multiple_errors(self):
        errors = ['error 1', 'error 2']
        res = SimpleResult(errors)
        self.assertTrue(type(res.errors) is list)
        for error in errors:
            self.assertTrue(error in res.errors)


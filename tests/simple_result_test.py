from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.results import SimpleResult

class ExampleTest(TestCase):
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
        res = SimpleResult(valid=False)

        self.assertFalse(res)
        self.assertTrue(not res)
        self.assertTrue(res == False)
        self.assertTrue(res != True)
        self.assertTrue(bool(res) is False)


    def test_simple_result_succes_evaluates_to_true(self):
        """ Truthy result evaluates to  boolean true"""
        res = SimpleResult(valid=True)

        self.assertTrue(res)
        self.assertTrue(res == True)
        self.assertTrue(res != False)
        self.assertTrue(bool(res) is True)


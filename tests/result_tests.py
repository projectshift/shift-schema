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

    def test_empty_result_is_true(self):
        """ result without errors evaluates to True"""
        result = Result()
        self.assertTrue(result)
        self.assertTrue(result == True)
        self.assertTrue(result != False)

    def test_result_with_errors_if_false(self):
        """ Result with errors evaluates to False """
        result = Result({'what?': 'error'})
        self.assertFalse(result)
        self.assertTrue(result == False)
        self.assertTrue(result != True)

    def test_raise_on_adding_bad_errors(self):
        """ Errors are type-checked before adding to result """
        self.fail()

    def test_add_single_error(self):
        """ Adding single error to Result """
        self.fail()

    def test_add_multiple_errors(self):
        """ Adding multiple errors to result """
        self.fail()

    def test_add_state_errors(self):
        """ Adding state errors to result """
        self.fail()

    def test_add_nested_results(self):
        """ Adding nested schema result on property """
        self.fail()

    def test_append_error_to_property(self):
        """ Appending errors to property"""
        self.fail()

    def test_type_check_merged(self):
        """ Check merged results before merging """
        self.fail()

    def test_merge_results(self):
        """ Merging one result into another """
        self.fail()


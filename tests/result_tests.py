from unittest import TestCase
from nose.plugins.attrib import attr

from shiftvalidate.result import Error, Result
from shiftvalidate.exceptions import InvalidErrorType, InvalidResultType

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
        result = Result({'what': 'error'})
        self.assertFalse(result)
        self.assertTrue(result == False)
        self.assertTrue(result != True)

    def test_raise_on_adding_bad_errors(self):
        """ Errors are type-checked before adding to result """
        result = Result()
        with self.assertRaises(InvalidErrorType):
            result.add_errors('Err')
        with self.assertRaises(InvalidErrorType):
            result.add_errors(['Err', 'Err'])


    def test_add_single_error(self):
        """ Adding single error to Result """
        result = Result()
        result.add_errors(Error('message'), 'property')
        self.assertTrue('property' in result.errors)

    def test_add_multiple_errors(self):
        """ Adding multiple errors to result """
        errors = [Error('error1'), Error('error2')]
        result = Result()
        result.add_errors(errors, 'property')
        self.assertEqual(2, len(result.errors['property']))

    def test_add_state_errors(self):
        """ Adding state errors to result """
        errors = [Error('error1'), Error('error2')]
        result = Result()
        result.add_errors(errors)
        self.assertEqual(2, len(result.errors['__state__']))

    def test_add_nested_results(self):
        """ Adding nested schema result on property """
        nested = Result()
        nested.add_errors(Error('message'))
        nested.add_errors(Error('message'), 'property')
        result = Result()
        result.add_nested_errors(nested, 'entity')
        self.assertTrue('entity' in result.errors)
        self.assertEqual(1, len(result.errors['entity']['__state__']))
        self.assertEqual(1, len(result.errors['entity']['property']))

    def test_append_error_to_property(self):
        """ Appending errors to property"""
        result1 = Result({'error': 'value'}) # simple
        errors1 = Error('single1')
        errors2 = Error('single2')
        result1.add_errors(errors1,'simple_property')
        result1.add_errors(errors2,'simple_property')
        self.assertTrue(errors1 in result1.errors['simple_property'])
        self.assertTrue(errors2 in result1.errors['simple_property'])

        result2 = Result({'error': 'value'}) # multi
        errors3 = [Error('multi1'), Error('multi2')]
        errors4 = [Error('multi3'), Error('multi4')]
        result2.add_errors(errors3, 'multi')
        result2.add_errors(errors4, 'multi')
        for e in errors3 + errors4:
            self.assertTrue(e in result2.errors['multi'])

        result3 = Result({'error': 'value'}) # state
        errors5 = [Error('state1'), Error('state2')]
        errors6 = [Error('state3'), Error('stat3')]
        result3.add_errors(errors5)
        result3.add_errors(errors6)
        for e in errors5 + errors6:
            self.assertTrue(e in result3.errors['__state__'])

    def test_type_check_merged(self):
        """ Check merged results before merging """
        result = Result()
        with self.assertRaises(InvalidResultType):
            result.merge(dict())

    def test_merge_results(self):
        """ Merging one result into another """

        p1 = [Error('prop1_error1'), Error('prop1_error2')]
        p2 = [Error('prop2_error1'), Error('prop2_error2')]
        s1 = [Error('state_error1'), Error('state_error2')]

        p22 = [Error('prop2_error3'), Error('prop2_error4')]
        p3 = [Error('prop3_error1'), Error('prop3_error2')]
        s2 = [Error('state_error3'), Error('state_error4')]

        result1 = Result()
        result1.add_errors(p1, 'property1')
        result1.add_errors(p2, 'property2')
        result1.add_errors(s1)

        result2 = Result()
        result2.add_errors(p22, 'property2')
        result2.add_errors(p3, 'property3')
        result2.add_errors(s2)

        result1.merge(result2)

        self.assertTrue(Error('prop1_error1') in result1.errors['property1'])
        self.assertTrue(Error('prop1_error2') in result1.errors['property1'])

        self.assertTrue(Error('prop2_error1') in result1.errors['property2'])
        self.assertTrue(Error('prop2_error2') in result1.errors['property2'])
        self.assertTrue(Error('prop2_error3') in result1.errors['property2'])
        self.assertTrue(Error('prop2_error4') in result1.errors['property2'])

        self.assertTrue(Error('prop3_error1') in result1.errors['property3'])
        self.assertTrue(Error('prop3_error2') in result1.errors['property3'])

        self.assertTrue(Error('state_error1') in result1.errors['__state__'])
        self.assertTrue(Error('state_error2') in result1.errors['__state__'])
        self.assertTrue(Error('state_error3') in result1.errors['__state__'])
        self.assertTrue(Error('state_error4') in result1.errors['__state__'])



from unittest import TestCase, mock
from nose.plugins.attrib import attr
from shiftvalidate.results import SimpleResult, ValidationResult

@attr('results', 'simple')
class SimpleResultTests(TestCase):
    """
    Simple result test
    This holds tests for the simple result
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
        """ Can set multiple errors on result """
        errors = ['error 1', 'error 2']
        res = SimpleResult(errors)
        self.assertTrue(type(res.errors) is list)
        for error in errors:
            self.assertTrue(error in res.errors)


@attr('results', 'validation')
class ValidationResultTests(TestCase):
    """
    Validation result tests
    This holds test for validation result aggregate
    """

    def test_create_validation_result(self):
        """ Can create validation result """
        res = ValidationResult()
        self.assertIsInstance(res, ValidationResult)

    def test_empty_result_evaluates_to_true(self):
        """ Empty result is valid """
        res = ValidationResult()

        self.assertTrue(res)
        self.assertTrue(res == True)
        self.assertTrue(res != False)

    def test_result_with_errors_evaluates_to_false(self):
        """ Result with errors is invalid """
        res = ValidationResult()
        res.errors['property'] = 'error'
        self.assertFalse(res)
        self.assertFalse(res == True)
        self.assertFalse(res != False)


    def test_add_single_error(self):
        """ Adding single error to result """
        error = 'me is single error'
        res = ValidationResult()
        res.add_errors(error, 'property')
        self.assertTrue(error in res.errors['property'])

    def test_add_multiple_errors(self):
        """ Adding multiple errors to result """
        errors = ['error 1', 'error 2']
        res = ValidationResult()
        res.add_errors(errors, 'property')
        for error in errors:
            self.assertTrue(error in res.errors['property'])


    def test_add_state_errors(self):
        """ Adding state errors to result """
        errors = ['error 1', 'error 2']
        res = ValidationResult()
        res.add_errors(errors)
        for error in errors:
            self.assertTrue(error in res.errors['__state__'])

    def test_can_append_to_existing_errors(self):
        """ Appending errors to existing set """

        # singles
        error1 = 'error 1'
        error2 = 'error 2'
        res1 = ValidationResult()
        res1.add_errors(error1, 'property')
        res1.add_errors(error2, 'property')
        self.assertEqual(2, len(res1.errors['property']))

        # multiples
        errors1 = ['error1', 'error2']
        errors2 = ['error3', 'error4']
        res2 = ValidationResult()
        res2.add_errors(errors1,'property')
        res2.add_errors(errors2,'property')
        self.assertEqual(4, len(res2.errors['property']))

        # state errors
        errors1 = ['error1', 'error2']
        errors2 = ['error3', 'error4']
        res3 = ValidationResult()
        res3.add_errors(errors1)
        res3.add_errors(errors2)
        self.assertEqual(4, len(res3.errors['__state__']))


    def test_raise_when_merging_bad_types(self):
        """ Raise error on merging incorrect object types """
        res1 = ValidationResult()
        res2 = dict()
        with self.assertRaises(TypeError):
            res1.merge(res2)


    def test_merging_two_results(self):
        """ Merging two result objects """

        result1 = ValidationResult()
        result1.add_errors(['prop1_error1', 'prop1_error2'], 'property1')
        result1.add_errors(['prop2_error1', 'prop2_error2'], 'property2')
        result1.add_errors(['state_error1', 'state_error2'])

        result2 = ValidationResult()
        result2.add_errors(['prop2_error3', 'prop2_error4'], 'property2')
        result2.add_errors(['prop3_error1', 'prop3_error2'], 'property3')
        result2.add_errors(['state_error3', 'state_error4'])

        # do it
        result1.merge(result2)

        self.assertTrue('prop1_error1' in result1.errors['property1'])
        self.assertTrue('prop1_error2' in result1.errors['property1'])

        self.assertTrue('prop2_error1' in result1.errors['property2'])
        self.assertTrue('prop2_error2' in result1.errors['property2'])
        self.assertTrue('prop2_error3' in result1.errors['property2'])
        self.assertTrue('prop2_error4' in result1.errors['property2'])

        self.assertTrue('prop3_error1' in result1.errors['property3'])
        self.assertTrue('prop3_error2' in result1.errors['property3'])

        self.assertTrue('state_error1' in result1.errors['__state__'])
        self.assertTrue('state_error2' in result1.errors['__state__'])
        self.assertTrue('state_error3' in result1.errors['__state__'])
        self.assertTrue('state_error4' in result1.errors['__state__'])


    def test_nest_result_on_property(self):
        """ Adding nested result on property """
        result1 = ValidationResult()
        result1.add_errors(['prop1_error1', 'prop1_error2'], 'property1')
        result1.add_errors(['prop2_error1', 'prop2_error2'], 'property2')
        result1.add_errors(['state_error1', 'state_error2'])

        result2 = ValidationResult()
        result2.add_errors(['prop2_error3', 'prop2_error4'], 'property2')
        result2.add_errors(['prop3_error1', 'prop3_error2'], 'property3')
        result2.add_errors(['state_error3', 'state_error4'])

        # do it
        result1.add_nested_errors('result2', result2)
        self.assertTrue('result2' in result1.errors)
        self.assertEqual(result2.errors, result1.errors['result2'])


    @attr('zz')
    def test_translate_result(self):
        """ Translating nested result with arbitrary translator"""

        result1 = ValidationResult()
        result1.add_errors('prop1_error1', 'property1')
        result1.add_errors(['prop2_error1', 'prop2_error2'], 'property2')
        result1.add_errors(['state_error1', 'state_error2'])

        result2 = ValidationResult()
        result2.add_errors(['prop2_error3', 'prop2_error4'], 'property2')
        result2.add_errors(['prop3_error1', 'prop3_error2'], 'property3')
        result2.add_errors(['state_error3', 'state_error4'])
        result1.add_nested_errors('result2', result2)

        def translator(input):
            return 'ZZZ' + input

        translated = result1.translate_errors(result1.errors, translator)

        # assert root translated
        self.assertEqual('ZZZprop1_error1', result1.errors['property1'][0])
        self.assertEqual('ZZZstate_error1', result1.errors['__state__'][0])

        # assert nested errors translated
        self.assertEqual(
            'ZZZprop3_error1',
            result1.errors['result2']['property3'][0]
        )

        self.assertEqual(
            'ZZZstate_error3',
            result1.errors['result2']['__state__'][0]
        )




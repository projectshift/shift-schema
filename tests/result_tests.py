from unittest import TestCase
from nose.plugins.attrib import attr

from shiftschema.result import Error, Result
from shiftschema import exceptions as x
from pprint import pprint as pp


@attr('result', 'result')
class ResultTest(TestCase):

    # --------------------------------------------------------------------------
    # basics
    # --------------------------------------------------------------------------

    def test_create_result(self):
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

    def test_result_with_errors_is_false(self):
        """ Result with errors evaluates to False """
        result = Result({'what': 'error'})
        self.assertFalse(result)
        self.assertTrue(result == False)
        self.assertTrue(result != True)

    # --------------------------------------------------------------------------
    # state validation errors errors
    # --------------------------------------------------------------------------

    def test_raise_on_adding_bad_state_errors(self):
        """ Raise on adding bad state errors """
        result = Result()
        with self.assertRaises(x.InvalidErrorType):
            result.add_state_errors('Err')
        with self.assertRaises(x.InvalidErrorType):
            result.add_state_errors(['Err', 'Err'])

    def test_add_single_state_error(self):
        """ Adding state errors to result """
        error = Error('error1')
        result = Result()
        result.add_state_errors(error)
        self.assertEqual(1, len(result.errors['__state__']))
        self.assertIn(error, result.errors['__state__'])

    def test_add_multiple_state_errors(self):
        """ Adding multiple state errors to result """
        errors = [Error('error1'), Error('error2')]
        result = Result()
        result.add_state_errors(errors)
        self.assertEqual(2, len(result.errors['__state__']))

    def test_append_state_errors(self):
        """ Appending state errors """
        e1 = Error('error 1')
        e2 = Error('error 2')
        e3 = Error('error 3')
        e4 = Error('error 4')

        result = Result()
        result.add_state_errors([e1, e2])
        result.add_state_errors([e3, e4])

        self.assertIn(e1, result.errors['__state__'])
        self.assertIn(e2, result.errors['__state__'])
        self.assertIn(e3, result.errors['__state__'])
        self.assertIn(e4, result.errors['__state__'])

    # --------------------------------------------------------------------------
    # simple property errors
    # --------------------------------------------------------------------------

    def test_raise_on_adding_bad_errors(self):
        """ Errors are type-checked before adding to result """
        result = Result()
        with self.assertRaises(x.InvalidErrorType):
            result.add_errors(errors='Err', property_name='prop')
        with self.assertRaises(x.InvalidErrorType):
            result.add_errors(errors=['Err', 'Err'], property_name='prop')

    def test_add_single_error(self):
        """ Adding single error to Result """
        result = Result()
        result.add_errors(errors=Error('message'), property_name='property')
        self.assertTrue('property' in result.errors)

    def test_add_multiple_errors(self):
        """ Adding multiple errors to result """
        errors = [Error('error1'), Error('error2')]
        result = Result()
        result.add_errors('property', errors)
        self.assertEqual(2, len(result.errors['property']))

    def test_append_simple_property_errors(self):
        """ Appending simple property errors """
        e1 = Error('error 1')
        e2 = Error('error 2')
        e3 = Error('error 3')
        e4 = Error('error 4')

        result = Result()
        result.add_errors('prop', [e1, e2])
        result.add_errors('prop', [e3, e4])

        self.assertIn(e1, result.errors['prop'])
        self.assertIn(e2, result.errors['prop'])
        self.assertIn(e3, result.errors['prop'])
        self.assertIn(e4, result.errors['prop'])

    # --------------------------------------------------------------------------
    # nested entity property errors
    # --------------------------------------------------------------------------

    def test_add_single_direct_error_to_nested_entity_errors(self):
        """ Adding single direct error to nested entity errors """
        error = Error('Direct entity error')
        result = Result()
        result.add_entity_errors('entity', direct_errors=error)
        self.assertIn('entity', result.errors)
        self.assertIn(error, result.errors['entity']['direct'])

    def test_add_multiple_direct_errors_to_nested_entity_errors(self):
        """ Adding multiple direct errors to nested entity errors """
        error1 = Error('Direct entity error 1')
        error2 = Error('Direct entity error 2')
        result = Result()
        result.add_entity_errors('entity', direct_errors=[error1, error2])
        self.assertIn('entity', result.errors)
        self.assertIn(error1, result.errors['entity']['direct'])
        self.assertIn(error2, result.errors['entity']['direct'])

    def test_raise_on_adding_bad_direct_errors_to_nested_entity_errors(self):
        """ Typecheck direct entity errors """
        result = Result()
        with self.assertRaises(x.InvalidErrorType):
            result.add_entity_errors('entity', direct_errors='Bad')
        with self.assertRaises(x.InvalidErrorType):
            result.add_entity_errors('entity', direct_errors=['Bad'])

    def test_append_direct_errors_to_nested_entity_errors(self):
        """ Appending direct errors to nested entity erorrs """
        e1 = Error('error 1')
        e2 = Error('error 2')
        e3 = Error('error 3')
        e4 = Error('error 4')

        result = Result()
        result.add_entity_errors('entity_property', direct_errors=[e1, e2])
        result.add_entity_errors('entity_property', direct_errors=[e3, e4])

        self.assertIn(e1, result.errors['entity_property']['direct'])
        self.assertIn(e2, result.errors['entity_property']['direct'])
        self.assertIn(e3, result.errors['entity_property']['direct'])
        self.assertIn(e4, result.errors['entity_property']['direct'])

    def test_add_schema_errors_to_nested_entity_property(self):
        """ Adding schema results to nested entity property"""
        e1 = Error('error 1')
        schema_errors = Result()
        schema_errors.add_errors('simple_prop', e1)
        result = Result()
        result.add_entity_errors('entity_prop', schema_errors=schema_errors)
        self.assertIn(e1, result.errors['entity_prop']['schema']['simple_prop'])

    def test_append_schema_errors_to_nested_entity_erors(self):
        """ Appending schema erros to nested entity erorrs """
        e1 = Error('error 1')
        e2 = Error('error 2')
        e3 = Error('error 3')
        e4 = Error('error 4')

        schema_errors1 = Result()
        schema_errors1.add_errors('simple_prop', [e1, e2])

        schema_errors2 = Result()
        schema_errors2.add_errors('simple_prop', [e3, e4])

        result = Result()
        result.add_entity_errors('entity_prop', schema_errors=schema_errors1)
        result.add_entity_errors('entity_prop', schema_errors=schema_errors2)

        self.assertIn(e1, result.errors['entity_prop']['schema']['simple_prop'])
        self.assertIn(e2, result.errors['entity_prop']['schema']['simple_prop'])
        self.assertIn(e3, result.errors['entity_prop']['schema']['simple_prop'])
        self.assertIn(e4, result.errors['entity_prop']['schema']['simple_prop'])

    def test_result_is_valid_when_nested_entity_valid(self):
        """ If nested entity is valid, result also valid """
        schema_errors = Result()
        result = Result()
        result.add_entity_errors('entity', schema_errors=schema_errors)
        self.assertTrue(result)

    # --------------------------------------------------------------------------
    # collection property errors
    # --------------------------------------------------------------------------


    def test_add_single_direct_error_to_nested_collection_errors(self):
        """ Adding single direct error to nested collection errors"""
        e1 = Error('error 1')
        result = Result()
        result.add_collection_errors('collection_prop', direct_errors=e1)
        self.assertIn(e1, result.errors['collection_prop']['direct'])

    def test_add_multiple_direct_errors_to_nested_collection_errors(self):
        """ Adding multiple direct error to nested collection errors"""
        e1 = Error('error 1')
        e2 = Error('error 2')
        result = Result()
        result.add_collection_errors('collection_prop', direct_errors=[e1, e2])
        self.assertIn(e1, result.errors['collection_prop']['direct'])
        self.assertIn(e2, result.errors['collection_prop']['direct'])

    def test_raise_on_adding_bad_direct_errs_to_nested_collection_errors(self):
        """ Typecheck direct collection errors """
        result = Result()
        with self.assertRaises(x.InvalidErrorType):
            result.add_collection_errors('collection', direct_errors='Bad')
        with self.assertRaises(x.InvalidErrorType):
            result.add_entity_errors('collection', direct_errors=['Bad'])

    def test_append_direct_errors_to_nested_collection_errors(self):
        """ Appending direct errors to nested collection errors """
        e1 = Error('error 1')
        e2 = Error('error 2')
        e3 = Error('error 3')
        e4 = Error('error 4')

        result = Result()
        result.add_collection_errors('collection_prop', direct_errors=[e1, e2])
        result.add_collection_errors('collection_prop', direct_errors=[e3, e4])

        self.assertIn(e1, result.errors['collection_prop']['direct'])
        self.assertIn(e2, result.errors['collection_prop']['direct'])
        self.assertIn(e3, result.errors['collection_prop']['direct'])
        self.assertIn(e4, result.errors['collection_prop']['direct'])

    def test_add_collection_errors_to_nested_collection_errors(self):
        """ Adding collection errors """
        e1 = Error('error 1')
        e2 = Error('error 2')

        collection_errors = [
            Result(errors=dict(simple=[e1])),
            Result(),
            Result(errors=dict(simple=[e2])),
            Result()
        ]

        result = Result()
        result.add_collection_errors(
            'collection_prop',
            collection_errors=collection_errors
        )

        errors = result.errors['collection_prop']['collection']
        self.assertIn(e1, errors[0].errors['simple'])
        self.assertIn(e2, errors[2].errors['simple'])

    # def test_append_collection_errors_to_nested_collection_errors(self):
    #     """ Appending direct errors to nested collection errors """
    #     self.fail('Implement me')

    def test_result_valid_when_nested_collection_valid(self):
        """ Do not create collection property on result if collection valid"""
        result = Result()
        result.add_collection_errors(
            'collection_prop',
            collection_errors=[Result(), Result()]
        )
        self.assertTrue(result)

    # --------------------------------------------------------------------------
    # merging results
    # --------------------------------------------------------------------------

    def test_raise_on_merging_incompatible_results(self):
        """ Raise on merging incompatible results """
        result1 = Result()
        result1.add_errors('property', [Error('Some Error')])

        result2 = Result()
        result2.add_entity_errors('property', direct_errors=[Error('Error')])

        with self.assertRaises(x.UnableToMergeResultsType):
            result1.merge(result2)

    def test_raise_on_merging_collection_into_entity(self):
        """ Raise on merging collection into entity"""
        result1 = Result()
        result1.errors = dict(prop=dict(schema=dict()))

        result2 = Result()
        result2.errors = dict(prop=dict(collection=dict()))

        with self.assertRaises(x.UnableToMergeResultsType):
            result1.merge(result2)

    def test_raise_on_merging_entity_into_collection(self):
        """ Raise on mergin entity into collection"""
        result1 = Result()
        result1.errors = dict(prop=dict(collection=dict()))

        result2 = Result()
        result2.errors = dict(prop=dict(schema=dict()))

        with self.assertRaises(x.UnableToMergeResultsType):
            result1.merge(result2)

    def test_merging_nested_results(self):
        """ Merging nested results"""

        # todo: test merging collections

        """
        Result 1
        """

        result1 = Result()

        # simple
        result1.add_errors('simple1', [
            Error('Res1 Simple prop1 err 1'),
            Error('Res1 Simple prop1 err 2'),
        ])

        # state
        result1.add_state_errors([
            Error('Res1 State 2'),
            Error('Res1 State 1')
        ])

        # entity direct
        result1.add_entity_errors('nested_entity1', direct_errors=[
            Error('Res1 Entity prop1 direct err 1'),
            Error('Res1 Entity prop1 direct err 2'),
        ])

        # entity nested schemas
        nested1_1 = Result()
        nested1_1.add_errors('nested_simple_1', [
            Error('Res1 Nested1 Simple1'),
            Error('Res1 Nested1 Simple2'),
        ])

        nested1_2 = Result()
        nested1_2.add_errors('deeper_nested_simple_1', [
            Error('Res1 Nested1 Simple1'),
            Error('Res1 Nested1 Simple2'),
        ])

        nested1_1.add_entity_errors('deeper', schema_errors=nested1_2)
        result1.add_entity_errors('nested_entity1', schema_errors=nested1_1)

        """
        Result 2
        """

        result2 = Result()

        # simple
        result2.add_errors('simple1', [
            Error('Res2 Simple prop1 err 3'),
            Error('Res2 Simple prop1 err 4'),
        ])

        result2.add_errors('simple2', [
            Error('Res2 Simple prop2 err 1'),
            Error('Res2 Simple prop2 err 2'),
        ])

        # state
        result2.add_state_errors([
            Error('Res2 State 1'),
            Error('Res2 State 2')
        ])

        # entity direct
        result2.add_entity_errors('nested_entity1', direct_errors=[
            Error('Res2 Entity prop1 direct err 3'),
            Error('Res2 Entity prop1 direct err 4'),
        ])

        result2.add_entity_errors('nested_entity2', direct_errors=[
            Error('Res2 Entity prop2 direct err 1'),
            Error('Res2 Entity prop2 direct err 2'),
        ])

        # entity nested schemas
        nested2_1 = Result()
        nested2_1.add_errors('nested_simple_1', [
            Error('Res2 Nested1 Simple1'),
            Error('Res2 Nested1 Simple2'),
        ])

        nested2_2 = Result()
        nested2_2.add_errors('deeper_nested_simple_2', [
            Error('Res2 Nested1 Simple1'),
            Error('Res2 Nested1 Simple2'),
        ])

        nested2_1.add_entity_errors('deeper', schema_errors=nested2_2)
        result2.add_entity_errors('nested_entity1', schema_errors=nested2_1)

        # now merge
        result1.merge(result2)
        err = result1.errors

        # assert simple merged
        self.assertEqual(4, len(err['simple1']))
        self.assertEqual(2, len(err['simple2']))

        # assert state merged
        self.assertEquals(4, len(err['__state__']))

        # assert direct errors merged
        self.assertEquals(4, len(err['nested_entity1']['direct']))
        self.assertEquals(2, len(err['nested_entity2']['direct']))

        # assert nested entities merged
        self.assertEquals(
            4,
            len(err['nested_entity1']['schema']['nested_simple_1'])
        )

        # assert deeper nested entities merged
        self.assertEquals(
            4,
            len(err['nested_entity1']['schema']['nested_simple_1'])
        )

        # assert merged recursively
        self.assertIn(
            'deeper_nested_simple_2',
            err['nested_entity1']['schema']['deeper']['schema']
        )
        self.assertIn(
            'deeper_nested_simple_1',
            err['nested_entity1']['schema']['deeper']['schema']
        )

    # --------------------------------------------------------------------------
    # translating and formatting resuts
    # --------------------------------------------------------------------------

    # todo: fixme
    def test_translate_messages(self):
        """ Translating nested result with arbitrary translator"""
        pass
        # p1 = [Error('prop1_error1')]
        # p2 = [Error('prop2_error1', Error('prop2_error2'))]
        # s1 = [Error('state_error1'), Error('state_error2')]
        #
        # p22 = [Error('prop2_error3'), Error('prop2_error4')]
        # p3 = [Error('prop3_error1'), Error('prop3_error2')]
        # s2 = [Error('state_error3'), Error('state_error4')]
        #
        # result1 = Result()
        # result1.add_errors('property1', p1)
        # result1.add_errors('property2', p2)
        # result1.add_state_errors(s1)
        #
        # result2 = Result()
        # result2.add_errors('property2', p22)
        # result2.add_errors('property3', p3)
        # result2.add_state_errors(s2)
        # result1.add_entity_errors('result2', result2)
        #
        # def translator(input):
        #     return 'ZZZ' + input
        #
        # result1._translate_errors(result1.errors, translator)
        #
        # # assert root translated
        # self.assertEqual('ZZZprop1_error1', result1.errors['property1'][0])
        # self.assertEqual('ZZZstate_error1', result1.errors['__state__'][0])
        #
        # # assert nested errors translated
        # self.assertEqual(
        #     'ZZZprop3_error1',
        #     result1.errors['result2']['property3'][0]
        # )
        #
        # self.assertEqual(
        #     'ZZZstate_error3',
        #     result1.errors['result2']['__state__'][0]
        # )


    def test_formatting_messages(self):
        """ Error messages formatted with parameters (if any) """
        result = Result()

        no = 'Me has no params'
        no_params = None
        self.assertEqual(no, result.format_error(no, no_params))

        positional = 'I have positionals: one {} two {} and {}'
        positional_params = [1, 2, 3]
        self.assertEqual(
            positional.format(*positional_params),
            result.format_error(positional, positional_params)
        )

        named = 'I have named params {one} and {two}'
        named_params = dict(one='FIRST', two='SECOND')
        self.assertEqual(
            named.format(**named_params),
            result.format_error(named, named_params)
        )





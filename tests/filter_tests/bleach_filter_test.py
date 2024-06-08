from unittest import TestCase

from shiftschema.filters import Bleach


class BleachFilterTest(TestCase):
    """ String bleach sanitizing filter test"""

    def setUp(self):
        super().setUp()
        self.params = dict(
            tags=['a'],
            attributes=['href'],
            styles=['color'],
            protocols=['http', 'https'],
            strip=False,
            strip_comments=False
        )

    def test_create(self):
        """ Can create bleach filter """
        filter = Bleach()
        self.assertIsInstance(filter, Bleach)

    def test_pass_through_non_strings(self):
        """ Bleach: Pass through non-string values (don't do anything) """
        filter = Bleach()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

    def test_compose_params(self):
        """ Compose bleach params upon filter instantiation """
        filter = Bleach(**self.params)
        self.assertEquals(self.params, filter.bleach_params)

    def test_can_filter_tags(self):
        """ Bleach filter can filter out tags"""
        text = '<b><i>Example</i></b><!-- comment -->'
        filter = Bleach(tags=['b'], strip=True)
        filtered = filter.filter(text)
        expected = '<b>Example</b>'
        self.assertEquals(expected, filtered)

    def test_can_filter_attributes(self):
        """ Bleach filter can filter out attributes"""
        text = '<b><a href="" target="_blank">Example</a></b>'
        filter = Bleach(
            tags=['a'],
            attributes=dict(a=['href', 'title'])
        )
        filtered = filter.filter(text)
        expected = '<a href="">Example</a>'
        self.assertEquals(expected, filtered)

    def test_can_filter_inline_styles(self):
        """ Bleach filter can filter out inline styles"""
        text = '<a href="" style="color: red; border: 1px">Example</a>'
        filter = Bleach(
            tags=['a'],
            attributes=['style', 'href'],
            styles=['color'],
        )
        filtered = filter.filter(text)
        expected = '<a href="" style="color: red;">Example</a>'
        self.assertEquals(expected, filtered)

    def test_can_filter_inline_styles(self):
        """ Bleach filter can filter out inline styles"""
        text = '<a href="https://google.com">Example</a>'
        filter = Bleach(
            tags=['a'],
            attributes=['href'],
            protocols=['http'],
        )
        filtered = filter.filter(text)
        expected = '<a>Example</a>'

        # assert link removed as protocol was invalid
        self.assertEquals(expected, filtered)






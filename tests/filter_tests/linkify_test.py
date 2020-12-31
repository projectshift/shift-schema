from unittest import TestCase, mock
from nose.plugins.attrib import attr

from shiftschema.filters import Linkify


@attr('filter', 'linkify')
class LinkifyTest(TestCase):
    """ String linkifier filter test"""

    def setUp(self):
        super().setUp()

        def linkify_callback(attrs, new=False):
            attrs[(None, 'title')] = 'Link in user test'
            return attrs

        self.params = dict(
            parse_email=False,
            callbacks=[linkify_callback],
            skip_tags=['pre']
        )

    def test_create(self):
        """ Can create linkify filter """
        filter = Linkify()
        self.assertIsInstance(filter, Linkify)

    def test_pass_through_non_strings(self):
        """ Linkify: Pass through non-string values (don't do anything) """
        filter = Linkify()
        self.assertEquals(None, filter.filter(None))
        self.assertEquals(False, filter.filter(False))
        self.assertEquals(123, filter.filter(123))

    def test_compose_params(self):
        """ Compose linkifier params upon filter instantiation """
        filter = Linkify(**self.params)
        self.assertEquals(self.params, filter.linkify_params)

    def test_linkify_urls(self):
        """ Linkify URLs in text"""
        text = 'Google: https://google.com'
        filter = Linkify()
        filtered = filter.filter(text)
        expected = 'Google: <a href="https://google.com">https://google.com</a>'
        self.assertEquals(expected, filtered)

    def test_linkify_emails(self):
        """ Linkify emails in text"""
        text = 'My email: test@test.com'
        filter = Linkify(parse_email=True)
        filtered = filter.filter(text)
        expected = 'My email: <a href="mailto:test@test.com">test@test.com</a>'
        self.assertEquals(expected, filtered)

    def test_linkify_adds_custom_attributes(self):
        """ Adding custom link attributes via linkifier callbacks"""
        text = 'My email: test@test.com'

        def add_class(attrs, new=False):
            attrs[(None, 'class')] = 'external'
            return attrs

        filter = Linkify(
            parse_email=True,
            callbacks=[add_class]
        )
        filtered = filter.filter(text)

        expected = 'My email: '
        expected += '<a class="external" href="mailto:test@test.com">'
        expected += 'test@test.com</a>'
        self.assertEquals(expected, filtered)

    def test_likifier_skips_tags(self):
        """ Linkifier skips linkifying within defined tags"""
        text = 'Google: https://google.com'
        text += '<pre>https://yahoo.com</pre>'

        filter = Linkify(skip_tags=['pre'])
        filtered = filter.filter(text)

        expected = 'Google: <a href="https://google.com">https://google.com</a>'
        expected += '<pre>https://yahoo.com</pre>'
        self.assertEquals(expected, filtered)




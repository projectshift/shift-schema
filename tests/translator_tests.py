from unittest import TestCase
from nose.plugins.attrib import attr

import os
from shiftvalidate.translator import Translator
from shiftvalidate.exceptions import NoTranslations

@attr('translator')
class TranslatorTests(TestCase):

    def test_create_translator(self):
        """ Creating a translator """
        trans = Translator()
        self.assertIsInstance(trans, Translator)

    def test_set_default_path_to_translations(self):
        """ Translator has default path to translations """
        dir = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.realpath(dir + '/../')
        dir = os.path.join(dir, 'shiftvalidate', 'translations')

        trans = Translator()
        self.assertTrue(dir in trans.dirs)

    def test_normalize_locale(self):
        """ Normalizing locales """
        locale1 = 'en_US'
        locale2 = 'EN-GB'
        locale3 = 'en'

        trans = Translator()
        self.assertEqual('en', trans.normalize_locale(locale1))
        self.assertEqual('en', trans.normalize_locale(locale2))
        self.assertEqual('en', trans.normalize_locale(locale3))

    def test_append_custom_translations_dir(self):
        """ Appending custom dir with translations """
        dir = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.join(dir, '_assets', 'translations')
        trans = Translator()
        trans.add_location(dir)
        self.assertTrue(dir in trans.dirs)

    def test_get_preloaded_translations(self):
        """ Return preloaded translations if present """
        translations = 'me is a language dictionary'
        trans = Translator()
        trans.translations['en'] = translations
        self.assertEqual(translations, trans.get_translations('EN_US'))

    def test_delete_preloaded_translations_when_adding_new_path(self):
        """ Clear preloaded translations when adding new path """
        translations = 'me is a language dictionary'
        trans = Translator()
        trans.translations['en'] = translations

        dir = os.path.dirname(os.path.realpath(__file__))
        dir = os.path.join(dir, '_assets', 'translations')
        trans.add_location(dir)
        self.assertFalse('en' in trans.translations)

    def test_raise_if_no_translations(self):
        """ Raise error if no translations found for locale """
        trans = Translator()
        with self.assertRaises(NoTranslations):
            trans.get_translations('not_locale')

    def test_loading_default_translations(self):
        """ Loading default translations for locale """
        trans = Translator()
        translations = trans.get_translations('EN_US')
        self.assertTrue('__meta__' in translations)

    def test_merge_custom_translations_with_default(self):
        """ Merging custom dictionaries with default """
        trans = Translator()

        custom = os.path.dirname(os.path.realpath(__file__))
        custom = os.path.join(custom, '_assets', 'translations')
        trans.add_location(custom)

        translations = trans.get_translations('ru_RU')
        meta = translations['__meta__']
        self.assertTrue(meta.startswith('Custom'))

    def test_translate_message(self):
        """ Translating a message """
        message = '__meta__'
        trans = Translator()
        translation = trans.translate(message, 'en')
        self.assertEqual('Default translations for English', translation)

    def test_return_untranslated(self):
        """ Return original message if no translation """
        trans = Translator()
        msg = 'no-translation-for-me'
        self.assertEqual(msg, trans.translate(msg, 'en'))

























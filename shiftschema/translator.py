import os
from importlib.machinery import SourceFileLoader
from shiftschema.exceptions import NoTranslations


class Translator:
    """
    Translator
    Manages translation dictionaries and performs translation of messages
    in an extensible way.
    """
    def __init__(self):
        """
        Initialize translator
        :return:                None
        """
        dir = os.path.dirname(os.path.realpath(__file__))
        self.dirs = [os.path.join(dir, 'translations')]
        self.translations = {}

    @staticmethod
    def normalize_locale(locale):
        """
        Normalize locale
        Extracts language code from passed in locale string to be used later
        for dictionaries loading.

        :param locale:          string, locale (en, en_US)
        :return:                string, language code
        """
        import re
        match = re.match(r'^[a-z]+', locale.lower())
        if match:
            return match.group()


    def add_location(self, dir):
        """
        Add location
        Adds location of locale dictionaries. Must be an existing directory as
        it will be later scanned for locale dictionaries. Adding a new
        location removes previously loaded translations.

        :param dir:             str, path to dir with translations
        :return:                None
        """
        self.translations = {}
        self.dirs.append(dir)


    def get_translations(self, locale):
        """
        Get translation dictionary
        Returns a dictionary for locale or raises an exception if such can't
        be located. If a dictionary for locale was previously loaded returns
        that, otherwise goes through registered locations and merges any
        found custom dictionaries with defaults.

        :param locale:          str, locale to load translations
        :return:                dict, translations dictionary
        """
        locale = self.normalize_locale(locale)
        if locale in self.translations:
            return self.translations[locale]

        translations = {}
        for path in self.dirs:
            file = os.path.join(path, '{}.py'.format(locale))
            if not os.path.isfile(file):
                continue

            loader = SourceFileLoader(locale, file)
            locale_dict = loader.load_module()
            if not hasattr(locale_dict, 'translations'):
                continue

            language = getattr(locale_dict, 'translations')
            if translations:
                translations = language
            else:
                merged = dict(translations.items() | language.items())
                translations = merged

        if translations:
            self.translations[locale] = translations
            return translations

        err = 'No translations found for locale [{}]'
        raise NoTranslations(err.format(locale))



    def translate(self, message, locale):
        """
        Translate
        Translates a message to the given locale language. Will return original
        message if no translation exists for the message.

        :param message:         str, a message to translate
        :param locale:          str, locale or language code
        :return:                str, translated (if possible)
        """
        translations = self.get_translations(locale)
        if message in translations:
            return translations[message]

        # return untranslated
        return message

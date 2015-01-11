import os
from importlib.machinery import SourceFileLoader
from shiftvalidate.exceptions import NoTranslations


class Translator:
    def __init__(self):
        dir = os.path.dirname(os.path.realpath(__file__))
        self.dirs = [os.path.join(dir, 'translations')]
        self.translations = {}

    @staticmethod
    def normalize_locale(locale):
        import re
        match = re.match(r'^[a-z]+', locale.lower())
        if match:
            return match.group()

    def add_location(self, dir):
        if os.path.isdir(dir):
            self.translations = {}
            self.dirs.append(dir)


    def get_translations(self, locale):
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
        translations = self.get_translations(locale)
        if message in translations:
            return translations[message]

        # return untranslated
        return message

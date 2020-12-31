from shiftschema.filters import AbstractFilter
from slugify import slugify


class Slugify(AbstractFilter):
    """
    Slugify filter
    Uses python-slugify library to create a url-compatible slug from the
    given text.
    """

    # convert html entities to unicode
    entities = True

    # converts html decimal to unicode
    decimal = True

    # converts html hexadecimal to unicode
    hexadecimal = True

    # output string length
    max_length = 0

    # truncates to end of full words
    word_boundary = False

    # return whole words in the initial order (max_length > 0)
    save_order = False

    # url word separator
    separator = '-',

    # words to discount
    stopwords = ()

    # regex pattern for allowed characters
    regex_pattern = None

    # force lowercase
    lowercase = True

    # list of replacement rules
    replacements = ()

    def __init__(
        self,
        *_,
        entities=True,
        decimal=True,
        hexadecimal=True,
        max_length=0,
        word_boundary=False,
        save_order=False,
        separator='-',
        stopwords=(),
        regex_pattern=None,
        lowercase=True,
        replacements=()
    ):
        """
        Initialise filter
        Accepts input keyword arguments to allow overriding defaults
        """
        self.entities = entities
        self.decimal = decimal
        self.hexadecimal = hexadecimal
        self.max_length = max_length
        self.word_boundary = word_boundary
        self.save_order = save_order
        self.separator = separator
        self.stopwords = stopwords
        self.regex_pattern = regex_pattern
        self.lowercase = lowercase
        self.replacements = replacements

    def filter(self, value, model=None, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param model:               parent model being validated
        :param context:             object, filtering context
        :return:                    filtered value
        """

        # string filter: skip non-strings
        if type(value) is not str:
            return value

        result = slugify(
            value,
            entities=self.entities,
            decimal=self.decimal,
            hexadecimal=self.hexadecimal,
            max_length=self.max_length,
            word_boundary=self.word_boundary,
            save_order=self.save_order,
            separator=self.separator,
            stopwords=self.stopwords,
            regex_pattern=self.regex_pattern,
            lowercase=self.lowercase,
            replacements=self.replacements,
        )
        return result



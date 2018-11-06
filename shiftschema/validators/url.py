from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import re


class Url(AbstractValidator):
    """
    URL validator
    """

    # default error message
    url_invalid = '%url_invalid%'

    # valid protocols
    protocols = ('http', 'https')

    # regex compile flags
    flags = re.UNICODE | re.IGNORECASE

    # allow localhost?
    localhost = False

    def __init__(self, protocols=None, localhost=False, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param protocols:       list, allowed protocols
        :param localhost:       bool, wether to allow localhost
        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.not_email = message

        if protocols:
            self.protocols = protocols

        if localhost:
            self.localhost = True

    def validate(self, value, model=None, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check
        :param model:           parent model being validated
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """
        value = str(value)
        regex = self.regex(
            protocols=self.protocols,
            localhost=self.localhost
        )

        regex = re.compile(regex, flags=self.flags)
        match = regex.match(value)

        # return error
        if not match:
            return Error(self.url_invalid)

        # success otherwise
        return Error()

    def regex(self, protocols, localhost=True):
        """
        URL Validation regex
        Based on regular expression by Diego Perini (@dperini) and provided
        under MIT License: https://gist.github.com/dperini/729294
        :return:
        """
        p = r"^"

        # protocol
        p += r"(?:(?:(?:{}):)?//)".format('|'.join(protocols))

        # basic auth (optional)
        p += r"(?:\S+(?::\S*)?@)?"

        p += r"(?:"

        # ip exclusion: private and local networks
        p += r"(?!(?:10|127)(?:\.\d{1,3}){3})"
        p += r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        p += r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"

        # ip excluding loopback (0.0.0.0), reserved space (244.0.0.0)
        # and network/broadcast addresses
        p += r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        p += r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        p += r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        p += r"|"

        # hostname
        p += r"(?:"
        p += r"(?:"
        p += r"[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?"
        p += r"[a-z0-9\u00a1-\uffff]"
        p += r"\." if not localhost else r"[\.]?|localhost"


        p += r")+"

        # tld
        p += r"(?:[a-z\u00a1-\uffff]{2,}\.?)"
        p += r")"

        # port (optional)
        p += r"(?::\d{2,5})?"

        # path (optional)
        p += r"(?:[/?#]\S*)?"

        p += r"$"
        return p






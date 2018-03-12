from shiftschema.validators.abstract_validator import AbstractValidator
from shiftschema.result import Error
import re


class Email(AbstractValidator):
    """
    Email validator
    Validates that passed in value is a valid email. The check is regex only
    so we don't do any MX checks here
    """

    not_email = '%email_invalid%'

    def __init__(self, message=None):
        """
        Initialize validator
        Accepts an optional custom error message.

        :param message:         str, custom error message
        :return:                None
        """
        if message is not None:
            self.not_email = message

    def validate(self, value, context=None):
        """
        Validate
        Perform value validation and return result

        :param value:           value to check
        :param context:         object or None, validation context
        :return:                shiftschema.results.SimpleResult
        """

        regex = self.regex()
        match = regex.match(value)
        if not match:
            return Error(self.not_email)

        # success otherwise
        return Error()

    def regex(self):
        """
        RFC822 Email Address Regex
        Originally written by Cal Henderson
        c.f. http://iamcal.com/publish/articles/php/parsing_email/
        Translated to Python by Tim Fletcher with changes suggested by Dan Kubb
        http://tfletcher.com/lib/rfc822.py
        Licensed under a Creative Commons Attribution-ShareAlike 2.5 License
        http://creativecommons.org/licenses/by-sa/2.5/

        :return:
        """

        qtext = '[^\\x0d\\x22\\x5c\\x80-\\xff]'
        dtext = '[^\\x0d\\x5b-\\x5d\\x80-\\xff]'

        atom = '[^\\x00-\\x20\\x22\\x28\\x29\\x2c\\x2e\\x3a-\\x3c\\x3e\\x40'
        atom += '\\x5b-\\x5d\\x7f-\\xff]+'

        quoted_pair = '\\x5c[\\x00-\\x7f]'
        domain_literal = "\\x5b(?:%s|%s)*\\x5d" % (dtext, quoted_pair)
        quoted_string = "\\x22(?:%s|%s)*\\x22" % (qtext, quoted_pair)
        domain_ref = atom
        sub_domain = "(?:%s|%s)" % (domain_ref, domain_literal)
        word = "(?:%s|%s)" % (atom, quoted_string)
        domain = "%s(?:\\x2e%s)*" % (sub_domain, sub_domain)
        local_part = "%s(?:\\x2e%s)*" % (word, word)
        addr_spec = "%s\\x40%s" % (local_part, domain)

        email_address = re.compile('\A%s\Z' % addr_spec)
        return email_address




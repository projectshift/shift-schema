from shiftschema.filters import AbstractFilter
import bleach


class Bleach(AbstractFilter):
    """
    Bleach filter
    Sanitizes incoming untrusted HTML based on an allowed attributes list.
    Can be used to escape or strip markup and attributes on content coming
    from untrusted sources.

    This is for sanitizing in HTML-context only. It is not safe to use bleach
    output outside of such content, e.g. in javascript or html attributes:

    Not safe: <body data-bio="{{ bleach.clean(user_bio} }}">

    See bleach documentation at: https://bleach.readthedocs.io
    """

    # list of allowed tags
    # default: bleach.sanitizer.ALLOWED_TAGS
    tags = None

    # allowed attributes (callable, list or dict)
    # default: bleach.sanitizer.ALLOWED_ATTRIBUTES
    attributes = None

    # allowed list of css styles
    # default: bleach.sanitizer.ALLOWED_STYLES
    styles = None

    # allowed list of protocols for links
    # default: bleach.sanitizer.ALLOWED_PROTOCOLS
    protocols = None

    # whether to strip disallowed elements (escapes otherwise)
    strip = True

    # whether to strip comments
    strip_comments = True

    # a dict of prepared bleach params containing all of the above
    bleach_params = None

    def __init__(
        self,
        tags=None,
        attributes=None,
        styles=None,
        protocols=None,
        strip=True,
        strip_comments=True
    ):
        """
        Initialize the filter and set bleach config options

        :param tags: allowed tag list
        :param attributes: allowed attributes list, dict or callable
        :param styles: allowed styles
        :param protocols: allowed protocols for links
        :param strip: strip disallowed elements?
        :param strip_comments: strip comments?
        """
        self.tags = tags
        self.attributes = attributes
        self.styles = styles
        self.protocols = protocols
        self.strip = strip
        self.strip_comments = strip_comments

        # prepare bleach params
        self.bleach_params = dict(
            strip=self.strip,
            strip_comments=self.strip_comments
        )

        if self.tags:
            self.bleach_params['tags'] = self.tags
        if self.attributes:
            self.bleach_params['attributes'] = self.attributes
        if self.styles:
            self.bleach_params['styles'] = self.styles
        if self.protocols:
            self.bleach_params['protocols'] = self.protocols

    def filter(self, value, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param context:             object, filtering context
        :return:                    filtered value
        """
        value = str(value)
        return bleach.clean(text=value, **self.bleach_params)



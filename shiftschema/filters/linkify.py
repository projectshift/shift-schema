from shiftschema.filters import AbstractFilter
from bleach.linkifier import Linker


class Linkify(AbstractFilter):
    """
    Linkify filter
    Will scan through text and find things that look like URLs or email
    addresses and ann links to them.

    See bleach documentation at: https://bleach.readthedocs.io

    See linkify documentation to see how callbacks work:
    https://bleach.readthedocs.io/en/latest/linkify.html
    """

    # list of callbacks to apply
    # default: bleach.linkifier.DEFAULT_CALLBACKS
    callbacks = None

    # skips links within tags given in this list
    skip_tags = None

    # whether to linkify email addresses
    parse_email = True

    # prepared list of params for linkifier containing all of the above
    linkify_params = None

    def __init__(self, callbacks=None, skip_tags=None, parse_email=True):
        """
        Initialize the filter and set bleach linkifier config options

        :param callbacks: list of callbacks
        :param skip_tags: list - skips links within these tags
        :param parse_email: bool - whether to linkify emails
        """

        self.callbacks = callbacks
        self.skip_tags = skip_tags
        self.parse_email = parse_email

        # prepare bleach params
        self.linkify_params = dict(parse_email=self.parse_email)
        if self.skip_tags:
            self.linkify_params['skip_tags'] = self.skip_tags

        # default linkify callback (does not add anything to attrs)
        if self.callbacks:
            self.linkify_params['callbacks'] = self.callbacks
        else:
            def default_callback(attrs, new=False):
                return attrs
            self.linkify_params['callbacks'] = [default_callback]

    def filter(self, value, context=None):
        """
        Filter
        Performs value filtering and returns filtered result.

        :param value:               input value
        :param context:             object, filtering context
        :return:                    filtered value
        """
        value = str(value)
        linker = Linker(**self.linkify_params)
        return linker.linkify(value)



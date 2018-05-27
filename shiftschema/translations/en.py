"""
English
Holds validation messages for the english language
"""
translations = {
    '__meta__': 'Default translations for English',

    # required
    '%value_required%': "Value required, can't be empty.",

    # choice
    '%choice_not_valid%': "Provided value is not a valid choice",


    # multichoice
    '%invalid_multichoice%': "Value contains invalid items: [{items}]",

    # digits
    '%digits_must_only_contain_digits%': "Must only consist of digits.",

    # length
    '%length_too_long%': "String is too long. Maximum is {max}",
    '%length_too_short%': "String is too short. Minimum is {min}",
    '%length_not_in_range%': "String length not in range {min}-{max} characters",

    # email
    '%email_invalid%': "This is not a valid email",

    # not empty
    '%not_iterable%': 'This is not an iterable',
    '%cant_be_empty%': 'Can\t be empty, at least one item required',
}

from flask_wtf import FlaskForm as FlaskWtf

class WtfSchemaMixin(FlaskWtf):
    _schema = None
    _force_context = None

    @property
    def schema(self): return self._schema

    @schema.setter
    def schema(self, value):self._schema = value

    def validate_on_submit(self):
        """ Extend validate on submit to allow validation with schema """

        # validate form
        valid = FlaskWtf.validate_on_submit(self)

        # return in case no schema or not submitted
        if not self._schema or not self.is_submitted():
            return valid

        # validate data with schema if got one and form was submitted
        data = dict()
        for field in self._fields:
            data[field] = self._fields[field].data

        result = self.schema.process(data, context=self._force_context)
        self.set_errors(result)

        # set filtered data back to form
        for field in data:
            self._fields[field].data = data[field]

        return valid and not bool(self.errors)




    def set_errors(self, result):
        """ Populate field errors with errors from schema validation """

        # todo: use wtf locale
        errors = result.get_messages()

        for property_name in errors:
            if not hasattr(self, property_name):
                continue # ignore errors for missing fields

            prop_errors = errors[property_name]
            if type(prop_errors) is not list:
                prop_errors = ['<Nested schema result following...>']
            if property_name in self.errors:
                self.errors[property_name].extend(prop_errors)
            else:
                self.errors[property_name] = prop_errors



class Form(WtfSchemaMixin, FlaskWtf):
    """
    Form
    Extends flask wtf form to allow setting schema on form
    """
    def __init__(self, *args, schema=None, context=None, **kwargs):
        self._schema = schema
        self._force_context = context
        FlaskWtf.__init__(self, *args, **kwargs)

from flask.ext.wtf import Form as FlaskWtf

class WtfSchemaMixin(FlaskWtf):
    _schema = None

    @property
    def schema(self): return self._schema

    @schema.setter
    def schema(self, value):self._schema = value

    def validate_on_submit(self):

        # validate form
        valid = FlaskWtf.validate_on_submit(self)

        # and schema
        if self._schema and self.is_submitted():
            data = {}
            for field in self._fields:
                data[field] = self._fields[field].data

            result = self.schema.process(data)

            # set filtered data back to form
            for field in data:
                self._fields[field].data = data[field]

            if not result:
                errors = result.get_messages() # todo: use wtf locale
                for property_name in errors:
                    prop_errors = errors[property_name]
                    if type(prop_errors) is not list:
                        prop_errors = ['<Nested schema result following...>']
                    if property_name in self.errors:
                        self.errors[property_name].extend(prop_errors)
                    else:
                        self.errors[property_name] = prop_errors

            return valid and bool(result)

        return valid


class Form(WtfSchemaMixin, FlaskWtf):
    def __init__(self, *args, schema=None, **kwargs):
        self._schema = schema
        FlaskWtf.__init__(self, *args, **kwargs)

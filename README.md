[![Build Status](https://api.travis-ci.org/projectshift/shift-validate.svg)](https://travis-ci.org/projectshift/shift-validate)

shift-validate
==============

Entity validation library for Python3. Can filter and validate data in model 
objects and simple dictionaries with flexible schemas. 

Why: validation and filtering of incoming data with form objects seems to be
the trend in web frameworks but it never felt right.

Main idea: decouple filtering and validation rules from web forms into
flexible shemas, then reuse those shemas in forms as well as apis and cli.

schema:
======

Schema is a collection of rules to filter and validate properties of your
model (object or dictionary). There are several ways to create a schema
the simples being initialization from spec dictionary:

```python
from shiftvalidate.schema import Schema
shiftvalidate import validators as validator

schema = Schema({
    'name' = dict(
        required=True,
        validators = [validator.Length(min=3, max=100)]
    ),
    'name' = dict(
        required=True,
        validators = [validator.Email()]
    )
})
```

Alternatively you can create a schema by subclassing Schema object:

```python
from shiftvalidate.schema import Schema
shiftvalidate import validators as validator

class MySchema(Schema):
    def schema(self):
        self.add_property('name')
        self.name.required=True
        self.name.add_validator(validator.Length(min=3, max=100))
        
        self.add_property('email')
        self.email.add_validator(validator.Email)

schema = MySchema()
```
You can then use this schema to filter and validate your model data, or `process` it (filter and validate as single operation).
To validate a model pass it to your schema and get back `Result`:

```python
model = dict(name=None, email='BAD')
valid = schema.validate(model)
print(valid == True) # False - validaation failed
print(valid.errors) # errors: name='Required', email='Invalid'
```

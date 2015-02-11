#!/usr/bin/env python3
import os
from setuptools import setup, find_packages


version = '0.0.7'


# monkey patch os for vagrant hardlinks
del os.link


# prepare config
config = dict(

    # author
    author = 'Dmitry Belyakov',
    author_email='dmitrybelyakov@gmail.com',

    # project meta
    name='shiftschema',
    version=version,
    url = 'https://github.com/projectshift/shift-schema',
    download_url='https://github.com/projectshift/shift-schema/tarball/'+version,
    description='Python3 filtering and validation library',
    keywords=['python3', 'validation', 'filtering', 'schema'],

    # license
    license='MIT',

    # packages
    packages=find_packages(exclude=['tests']),

    # dependencies
    install_requires=[]

)

# finally run the setup
setup(**config)

# register: ./setup.py register -r pypi
# build: ./setup.py sdist
# upload: ./setup.py upload -r pypi

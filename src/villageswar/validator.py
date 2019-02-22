from jsonschema import validate
from pkgutil import get_data
from json import loads
from os.path import join


def validate_config(json):
    validate(json, config_schema)
    return json


def validate_generator(json):
    validate(json, generator_schema)
    return json


def load_config_schema():
    return loads(
        get_data('villageswar', join('res', 'schema', 'config_schema.json'))
    )


def load_generator_schema():
    return loads(
        get_data('villageswar', join('res', 'schema', 'generator_schema.json'))
    )


config_schema = load_config_schema()

generator_schema = load_generator_schema()

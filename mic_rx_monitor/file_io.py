
from datetime import datetime
from os import makedirs, path

from strictyaml import as_document, load as yaml_load

from . import __config_file__
from .schema import config_schema


def load_yaml_file(filepath, schema):
    """Note: this function does not perform any handling of Errors or Exceptions."""
    with open(filepath, mode='r', encoding='utf-8') as filehandle:
        return yaml_load(
            filehandle.read(),
            schema,
            label=path.basename(filepath)
        ).data

def write_yaml_file(filepath, schema, content):
    yaml = as_document(content, schema)
    with open(filepath, mode='w', encoding='utf-8') as filehandle:
        return filehandle.write(
            yaml.as_yaml()
        )

def load_config_file():
    if path.exists(__config_file__):
        return load_yaml_file(__config_file__, config_schema)
    return create_blank_config()

def save_config_file(config):
    if not path.exists(__config_file__):
        makedirs(path.dirname(__config_file__), exist_ok=True)

    config['lastSave'] = datetime.utcnow()
    return write_yaml_file(__config_file__, config_schema, config)

def create_blank_config():
    return as_document(
        dict({
            "lastSave": datetime.min,
            "rx": list(),
        }),
        config_schema
    ).data

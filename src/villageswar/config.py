from pkgutil import get_data
from json import loads
from os.path import join
from villageswar.validator import validate_config, validate_generator
from villageswar.exception import InvalidConfigError, InvalidGeneratorError
from jsonschema import ValidationError

# Stores both custom and default configurations

configs = {
    
    'default_config': None,
    'config': None,
    'cmd-args': None,
    'next_id': 0,
    'default_generator': None,
    'generator': None
}

# Loads default config and generator

try:
    configs['default_config'] = validate_config(loads(get_data('villageswar',
                                                               join('res', 'default', 'default_config.json'))))
except ValidationError:
    raise InvalidConfigError('Default config is invalid')

try:
    configs['default_generator'] = validate_generator(loads(get_data('villageswar',
                                                                     join('res', 'default', 'default_generator.json'))))
except ValidationError:
    raise InvalidGeneratorError('Default generator is invalid')


def next_id():
    next_identifier = configs['next_id']
    configs['next_id'] += 1
    return str(next_identifier)


def get_config():
    # Returns either the custom or the default configurations
    
    return configs['config'] or configs['default_config']


def get_generator():
    # Returns either the custom or the default generators
    
    return configs['generator'] or configs['default_generator']


def get_cmd_args():
    # Returns the arguments passed by command line
    
    return configs['cmd-args']


def close_dump_file():
    # Closes dump file, if one was specified
    
    cmd_args = get_cmd_args()
    
    if cmd_args['dump-file']:
        # Closes dump file
        
        f = cmd_args['dump-file']
        cmd_args['dump-file'] = None
        f.close()


def stop():
    # Stops the execution of the main process
    
    close_dump_file()
    exit(0)

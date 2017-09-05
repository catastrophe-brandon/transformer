import json
import logging
import os
from json import JSONDecodeError

logger = logging.getLogger()


def validate_configuration(config_file):
    """Validate configuration details supplied via config_file."""
    try:
        config_data = json.load(open(config_file, 'r'))
    except JSONDecodeError as e:
        logger.error('Failed to decode JSON data from %s', config_file)
        raise e

    # Check the document for required keys/values
    # server
    assert config_data.get('server') is not None, 'server value in config incorrect'

    # user
    assert config_data.get('user') is not None, 'user value in config incorrect'

    # password
    assert config_data.get('password') is not None, 'password value in config incorrect'

    # database
    assert config_data.get('database') is not None, 'database value in config incorrect'

    assert config_data.get('successDir') is not None, 'successDir was incorrect'
    assert config_data.get('failureDir') is not None, 'failureDir was incorrect'
    return True


def load_configuration(config_file):
    """Validate config_file as a real file and load it as a dictionary."""
    assert os.path.isfile(config_file), '{} is not a file'.format(config_file)
    return json.load(open(config_file, 'r'))

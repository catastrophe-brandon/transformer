import json
import logging
from enum import Enum, unique
from json import JSONDecodeError

logger = logging.getLogger()


@unique
class ValidTypes(Enum):
    """ValidTypes represents the valid data types that can be expressed in the mapping config."""

    String = 1
    Integer = 2
    Decimal = 3
    Date = 4


def validate_mapping_configuration(mapping_config_file):
    """Return a MappingConfig object if the configuration is valid."""
    try:
        config_json = json.load(open(mapping_config_file, 'r'))
    except JSONDecodeError:
        logger.error('Failed to decode mapping configuration JSON')
        return None

    # main object should contain a list
    if config_json.get('columns') is None:
        logger.error('Configuration requires a list of columns')
        return None

    # 'columns' should contain at least one column
    if len(config_json.get('columns')) < 1:
        logger.error('Configuration requires at least one column')
        return None

    for column in config_json.get('columns'):
        assert column.get('dbColumnName') is not None, \
            'a column was missing the dbColumnName key'
        assert column.get('type') is not None, \
            'a column was missing the type key'
        assert is_valid_type(column.get('type')), \
            'Invalid type specified {}'.format(column.get('type'))

    # TODO: If CSV or TSV, confirm the entire range of indices is present
    # TODO: Else if XML, confirm an XPATH was provided
    # TODO: Confirm none of the objects have both inputIndex and XPATH

    return config_json


def is_valid_type(input_type):
    """Return true if the data type specified by the mapping config is valid."""
    if input_type in ValidTypes.__members__.keys():
        return True
    else:
        return False

import logging
import os

from .config_validation import load_configuration, validate_configuration
from .data_parser import CSVParserTabular, TSVParserTabular
from .data_validation import validate_tuple_data
from .database import connect, save_data, table_exists
from .file import FileType, file_type
from .mapping_validation import validate_mapping_configuration

logger = logging.getLogger()

DATABASE_CONN_TIMEOUT = 10


def load_data(file_path, mapping_file, destination_table, config_file):
    """Load data."""
    logger.debug('load_data called with {}, {}, {}, and {}'
                 .format(file_path, mapping_file, destination_table, config_file))
    assert os.path.isfile(file_path), '{} is not a file'.format(file_path)
    assert os.path.isfile(mapping_file), '{} is not a file'.format(file_path)
    assert os.path.isfile(config_file), '{} is not a file'.format(file_path)

    # Load and validate the mapping file
    mapping_config = validate_mapping_configuration(mapping_file)
    assert mapping_config is not None, 'Mapping configuration was invalid'

    # Load and validate the configuration
    configuration_valid = validate_configuration(config_file)
    assert configuration_valid, 'Processor configuration was invalid'

    configuration = load_configuration(config_file)
    logger.debug('Configuration loaded!')
    logger.debug('User: %s', configuration['user'])
    logger.debug('Password: %s', configuration['password'])

    # Determine the file type from the file_path
    file_type_value = file_type(file_path)
    assert file_type_value is not FileType.UNKNOWN, 'Input file contained an unknown type of data'

    # Parse the data to a series of tuples using the appropriate data parser
    if file_type_value is FileType.CSV:
        new_data = CSVParserTabular().parse_all(open(file_path, 'r').readlines())
    elif file_type_value is FileType.TSV:
        new_data = TSVParserTabular().parse_all(open(file_path, 'r').readlines())
    elif file_type_value is FileType.XML:
        # TODO: Add logic to parse all the columns then join everything together as
        # a list of tuples.
        raise NotImplementedError
    else:
        new_data = None

    assert len(new_data) > 0, 'The input data file was empty'

    # Confirm the destination table exists
    server = configuration.get('server')
    user = configuration.get('user')
    password = configuration.get('password')
    database = configuration.get('database')
    with connect(server=server, user=user, password=password, db_name=database, timeout=10) as conn:
        assert table_exists(conn, database, destination_table)

    # Validate the tuples based on the mapping configuration
    if not validate_tuple_data(new_data, mapping_config):
        logger.error('Invalid data was found in the input file. No data was processed.')
        return

    # Store the tuple data based on the mapping configuration
    with connect(server=server, user=user, password=password, db_name=database, timeout=10) as conn:
        save_data(conn, new_data, mapping_config, destination_table)

    # If data was stored successfully, move it to the successDir

    pass

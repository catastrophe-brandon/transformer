import contextlib
from datetime import datetime

import pytds

from .data_validation import DateValidator


@contextlib.contextmanager
def connect(server, user, password, db_name, timeout):
    """Connect to a SQL server using pytds."""
    args = {
        'dsn': server,
        'user': user,
        'password': password,
        'database': db_name,
        'as_dict': True,
        'autocommit': True,
        'login_timeout': timeout,
        'timeout': timeout,
    }

    with pytds.connect(**args) as conn:
        yield conn


def save_data(conn, list_of_tuples, mapping_configuration, table_name):
    """Save the given tuples to the database using the mapping configuration."""
    insert_sql = build_insert_sql(table_name, mapping_configuration, list_of_tuples)
    db_cursor = conn.cursor()
    db_cursor.execute(insert_sql)


def table_exists(conn, db_name, tbl_name):
    """Return True if the given table exists in the specified database."""
    cursor = conn.cursor()
    sql = 'SELECT COUNT(*) FROM {}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'{}\''\
        .format(db_name, tbl_name)
    result = cursor.execute_scalar(sql)
    return result == 1


def build_insert_sql(table_name, mapping_configuration, list_of_tuples):
    """Build the SQL to insert the data into the database."""
    insert_stmt = 'INSERT INTO {} '.format(table_name)
    columns_list = [item.get('dbColumnName') for item in mapping_configuration.get('columns')]
    columns_list = sorted(columns_list)
    columns_sql = '({})'.format(','.join(columns_list))
    values = ' VALUES '

    for some_tuple in list_of_tuples:
        values += str(reorder_tuple(some_tuple, columns_list, mapping_configuration)) + ', '

    values = values.rstrip(', ')
    return insert_stmt + columns_sql + values


def reorder_tuple(input_tuple, columns_list, mapping_config):
    """Return tuple contents reordered to match the mapping configuration."""
    result = [None for _ in range(len(input_tuple))]

    for column in mapping_config.get('columns'):
            input_index = column.get('inputIndex')
            input_type = column.get('type')
            result_index = columns_list.index(column.get('dbColumnName'))
            if input_type == 'String':
                result[result_index] = input_tuple[input_index]
            elif input_type == 'Integer':
                result[result_index] = int(input_tuple[input_index])
            elif input_type == 'Decimal':
                result[result_index] = float(input_tuple[input_index])
            elif input_type == 'Date':
                result[result_index] = datetime.strptime(input_tuple[input_index],
                                                         DateValidator.FORMAT_STRING)
            else:
                raise TypeError

    return tuple(result)

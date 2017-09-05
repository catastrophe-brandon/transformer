import pytest

from p5000.database import build_insert_sql
from p5000.mapping_validation import validate_mapping_configuration


@pytest.mark.skip(reason='Not ready yet')
def test_connect():
    """Test a connection to the database."""
    assert False


def test_build_insert_sql():
    """Test the build_insert_sql function."""
    table_name = 'some_table'
    mapping_configuration = validate_mapping_configuration('tests/assets/example_csv_mapping.json')
    list_of_tuples = [
        ('a', 5, 4, 3.0, 2.0, 1.0),
        ('g', 7, 8, 9.0, 10.0, 11.0)
    ]
    result = build_insert_sql(table_name, mapping_configuration, list_of_tuples)
    assert result == 'INSERT INTO some_table (blah,blah2,blah3,blah4,blah5,blah6) VALUES' \
                     ' (\'a\', 5, 4, 3.0, 2.0, 1.0), (\'g\', 7, 8, 9.0, 10.0, 11.0)'


def test_build_insert_sql_reversed_input():
    """Test the build_insert_sql function and remapping process."""
    table_name = 'some_table'
    mapping_configuration = validate_mapping_configuration('tests/assets/reverse_csv_mapping.json')
    list_of_tuples = [
        ('f', 6, 7, 8.0, 9.0, 10.0),
        ('l', 20, 21, 22.0, 23.0, 24.1)
    ]
    result = build_insert_sql(table_name, mapping_configuration, list_of_tuples)
    assert result == 'INSERT INTO some_table (blah,blah2,blah3,blah4,blah5,blah6) VALUES' \
                     ' (10.0, 9.0, 8.0, 7, 6, \'f\'), (24.1, 23.0, 22.0, 21, 20, \'l\')'


def test_reordered_csv_mapping():
    """Test the build_insert_sql function and remapping process."""
    table_name = 'some_table'
    # Semantically file contents are similar to the reverse file, column data was shuffled
    # in the JSON config
    # Results of test should be the same.
    mapping_configuration = \
        validate_mapping_configuration('tests/assets/reordered_csv_mapping.json')
    list_of_tuples = [
        ('f', 6, 7, 8.0, 9.0, 10.0),
        ('l', 20, 21, 22.0, 23.0, 24.1)
    ]
    result = build_insert_sql(table_name, mapping_configuration, list_of_tuples)
    assert result == 'INSERT INTO some_table (blah,blah2,blah3,blah4,blah5,blah6) VALUES' \
                     ' (10.0, 9.0, 8.0, 7, 6, \'f\'), (24.1, 23.0, 22.0, 21, 20, \'l\')'

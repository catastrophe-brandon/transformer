import pytds
import pytest

from p5000.p5000 import load_data


@pytest.mark.skip(reason='Not ready yet')
def test_p5000():
    """Happy path test."""
    data_file_path = 'tests/assets/example.csv'
    config_file = 'tests/assets/config.json'
    mapping_file = 'tests/assets/example_csv_mapping.json'
    destination_table = 'tacobell'

    ret_code = load_data(data_file_path, mapping_file, destination_table, config_file)
    assert ret_code == 0


def test_p5000_login_failure():
    """Confirm p5000 fails when given invalid login details."""
    data_file_path = 'tests/assets/example.csv'
    config_file = 'tests/assets/config.json'
    mapping_file = 'tests/assets/example_csv_mapping.json'
    destination_table = 'tacobell'

    with pytest.raises(pytds.tds_base.OperationalError):
        load_data(data_file_path, mapping_file, destination_table, config_file)

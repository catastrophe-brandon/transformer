from p5000.mapping_validation import is_valid_type, validate_mapping_configuration


def test_validate_mapping_file():
    """Test operation to validate the mapping file."""
    valid_mapping_file = 'tests/assets/example_csv_mapping.json'
    valid_config = validate_mapping_configuration(valid_mapping_file)
    assert valid_config is not None

    invalid_mapping_file = 'tests/assets/empty_file.json'
    invalid_config = validate_mapping_configuration(invalid_mapping_file)
    assert invalid_config is None


def test_is_valid_type():
    """Test the is_valid_type function."""
    assert is_valid_type('Integer')
    assert is_valid_type('String')
    assert is_valid_type('Decimal')
    assert is_valid_type('Date')

    assert not is_valid_type('pizza')
    assert not is_valid_type('tortuga')
    assert not is_valid_type('greg')

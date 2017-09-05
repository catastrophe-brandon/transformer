from json import JSONDecodeError

import pytest

from p5000.config_validation import load_configuration, validate_configuration


def test_validate_good_config():
    """Confirm a valid configuration passes validation."""
    assert validate_configuration('tests/assets/config.json')


def test_validate_bad_config():
    """Confirm an invalid configuration fails validation."""
    with pytest.raises(AssertionError):
        validate_configuration('tests/assets/bad_config.json')

    with pytest.raises(AssertionError):
        validate_configuration('tests/assets/bad_config2.json')


def test_validate_empty_config():
    """Confirm an empty config file fails."""
    with pytest.raises(JSONDecodeError):
        validate_configuration('tests/assets/empty_file.json')


def test_validate_non_json_config():
    """A non-json config file should fail with a friendly message."""
    non_json_config = 'tests/assets/bad_xml_config.xml'
    with pytest.raises(JSONDecodeError):
        validate_configuration(non_json_config)


def test_load_config_settings():
    """Test operation to load the configuration settings."""
    with pytest.raises(AssertionError):
        load_configuration('not_valid_file')

    config = load_configuration('tests/assets/config.json')
    assert config is not None

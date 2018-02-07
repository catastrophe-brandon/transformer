

from p5000.data_validation import (XPathValidator, validate_data, validate_single_tuple,
                                   validate_tuple_data)
from p5000.mapping_validation import validate_mapping_configuration


def test_xpath_validation_detects_bad_xpath():
    """Confirm an invalid XPATH is properly detected."""
    # invalid because the tag name isn't specified
    xpath = '[=\'something\']'
    assert XPathValidator().validate(xpath) is False


def test_xpath_validation_accepts_good_xpath():
    """Confirm the XPATH validator accepts good XPATH expressions."""
    xpath = '[sometag=\'somevalue\']'
    assert XPathValidator().validate(xpath)


def test_validate_tuple_data():
    """Test function to validate the tuple data."""
    mapping_config = validate_mapping_configuration('tests/assets/mapping_one_of_each.json')
    all_tuples = [('String', 1234, '2017-09-04', 3.1415)]
    assert validate_tuple_data(all_tuples, mapping_config)


def test_validate_tuple_data_with_bad_data():
    """Call validate_tuple_data using bad data."""
    mapping_config = validate_mapping_configuration('tests/assets/mapping_one_of_each.json')
    all_tuples = [('String', '2017-09-04', 1234, 3.1415)]
    assert not validate_tuple_data(all_tuples, mapping_config)


def test_validate_single_tuple():
    """Test function to validate a single tuple."""
    mapping_configuration = validate_mapping_configuration('tests/assets/mapping_one_of_each.json')
    single_tuple = ('Pizza', 6667, '2245-08-29', 2.73)
    assert validate_single_tuple(single_tuple, mapping_configuration)


def test_validate_single_tuple_bad_tuple():
    """Confirm function to validate a tuple fails when given a bad tuple."""
    mapping_configuration = validate_mapping_configuration('tests/assets/mapping_one_of_each.json')
    single_tuple = ('2245-08-29', 'Pizza', 2.73, 888)
    assert not validate_single_tuple(single_tuple, mapping_configuration)


def test_validate_data_good_integer():
    """Test function to validate one part of a tuple."""
    assert validate_data('1234567', 'Integer')


def test_validate_data_bad_integer():
    """Test function for validating integer data with a bad integer."""
    assert not validate_data('1234ab', 'Integer')


def test_validate_good_decimal():
    """Test function for validating good decimal data."""
    assert validate_data('123456.7890', 'Decimal')


def test_validate_bad_decimal():
    """Test function for validating bad decimal data."""
    assert not validate_data('123456a.012', 'Decimal')


def test_validate_good_date():
    """Confirm validator accepts good dates."""
    assert validate_data('2017-09-04', 'Date')


def test_validate_bad_date():
    """Confirm validator fails bad dates."""
    assert not validate_data('tacos tacos tacos', 'Date')

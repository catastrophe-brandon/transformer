
import pytest

from p5000.data_parser import CSVParserTabular, TSVParserTabular, XMLParser
from p5000.xml_input_validation import validate_xml_input


def test_csv_parser():
    """Test features of the CSVParser class."""
    csv_parser = CSVParserTabular()
    result = csv_parser.parse('a,b,c')
    assert len(result) == 3
    assert result == ('a', 'b', 'c')

    lines = ['a,b,c', 'd,e,f']
    tuple_list = csv_parser.parse_all(lines)
    assert tuple_list[0] == ('a', 'b', 'c')
    assert tuple_list[1] == ('d', 'e', 'f')


def test_tsv_parser():
    """Test features of the TSVParser class."""
    tsv_parser = TSVParserTabular()
    result = tsv_parser.parse('a\tb\tc')
    assert len(result) == 3
    assert result == ('a', 'b', 'c')

    lines = ['a\tb\tc', 'd\te\tf']
    tuple_list = tsv_parser.parse_all(lines)
    assert tuple_list[0] == ('a', 'b', 'c')
    assert tuple_list[1] == ('d', 'e', 'f')


def test_xml_parser():
    """Test features of the XMLParser class."""
    example_xml = 'tests/assets/example.xml'
    assert validate_xml_input(example_xml)

    results = XMLParser().parse_column_data(example_xml, './/name')
    assert len(results) == 2
    assert results[0] == 'Barney'
    assert results[1] == 'Judith'


def test_xml_parser_no_matches():
    """Test for correct behavior when no matches are found."""
    example_xml = 'tests/assets/example.xml'
    assert validate_xml_input(example_xml)

    with pytest.raises(AssertionError):
        XMLParser().parse_column_data(example_xml, 'barf')

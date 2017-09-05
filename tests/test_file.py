

from p5000.file import FileType, file_type


def test_file_type_checking():
    """Test file type checking process."""
    csv_file = 'tests/assets/example.csv'
    assert file_type(csv_file) == FileType.CSV

    tsv_file = 'tests/assets/example.tsv'
    assert file_type(tsv_file) == FileType.TSV

    xml_file = 'tests/assets/example.xml'
    assert file_type(xml_file) == FileType.XML

    unkownn_file = 'tests/assets/empty_file.json'
    assert file_type(unkownn_file) == FileType.UNKNOWN

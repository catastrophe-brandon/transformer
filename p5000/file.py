from enum import Enum

from p5000.xml_input_validation import validate_xml_input


class FileType(Enum):
    """An enumeration of different data file types."""

    CSV = 1
    TSV = 2
    XML = 3
    UNKNOWN = 37


def file_type(input_file):
    """Determine file type from provided file path based on content."""
    with open(input_file, 'r') as file:
        firstline = file.readline().strip()
        if firstline == '':
            return FileType.UNKNOWN
        elif ',' in firstline and len(firstline.split(',')) >= 1:
            return FileType.CSV
        elif '\t' in firstline and len(firstline.split('\t')) >= 1:
            return FileType.TSV
        elif validate_xml_input(input_file):
            return FileType.XML
        else:
            return FileType.UNKNOWN

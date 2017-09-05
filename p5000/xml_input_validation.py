from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import ParseError


def validate_xml_input(xml_document):
    """Validate a given XML file used as input."""
    parser = ET()
    try:
        parser.parse(source=xml_document)
        return True
    except ParseError:
        return False

from xml.etree.ElementTree import ElementTree as ET


class TabularDataParser(object):
    """
    DataParser defines a basic interface for different types of parser for input data.

    A given data parser should be able to accept lines of data from an input file and convert
    them to a list of tuples for consumption by a database.
    """

    def __init__(self):
        """Initialize the given DataParser object."""
        pass

    def parse(self, line):
        """Parse a single line of input for conversion to a single tuple."""
        pass

    def parse_all(self, series_of_lines):
        """Parse a series of lines of input for return as a list of tuples."""
        return [self.parse(line) for line in series_of_lines]


class CSVParserTabular(TabularDataParser):
    """Parses CSV data for conversion to a list of tuples."""

    SEPARATOR = ','

    def parse(self, line):
        """Parse a comma-separated line."""
        return tuple(line.split(self.SEPARATOR))


class TSVParserTabular(TabularDataParser):
    """Parses TSV data for conversion to a list of tuples."""

    SEPARATOR = '\t'

    def parse(self, line):
        """Parse a tab-separated line."""
        return tuple(line.split(self.SEPARATOR))


class XMLParser(TabularDataParser):
    """Parses XML data for conversion to a list of tuples."""

    def parse_column_data(self, xml_document, xpath):
        """
        Given the xpath to locate data for a column, pull all the data column as a list.

        @:param xml_document the XML document to be processed
        @:param xpath an XPATH specifying the relative location for all elements of a given type
                holding column data.

        Note: The XML document and XPATH are assumed to have been validated prior to invocation.
        """
        # Parse the XML document into an ElementTree
        parser = ET()
        tree = parser.parse(source=xml_document)

        # Find all the matches and confirm the list is not empty
        matches = tree.findall(xpath)
        assert len(matches) >= 1, 'No matching data was found in the document'

        # Return a list of all the text from the elements
        results = [element.text for element in matches]
        return results

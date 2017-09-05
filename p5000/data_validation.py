# Data validators for each type of data that can be stored in the DB go here.
import logging
from datetime import datetime
from xml.etree.ElementTree import XML

logger = logging.getLogger()


class DataValidator(object):
    """Base class to extend for building a data validator object."""

    def validate(self, input_data):
        """Validate the data provided. Method is intended to be overridden by class extension."""
        return False


class IntegerValidator(DataValidator):
    """Validates data of type Integer."""

    def validate(self, input_data):
        """Validate integer input data."""
        try:
            int(input_data)
            return True
        except ValueError:
            return False


class DateValidator(DataValidator):
    """Validates input data of type Date."""

    FORMAT_STRING = '%Y-%m-%d'
    # TODO: We may need to make a special base class and subclasses that
    # accept different strptime formats in the constructor for validating different timestamps

    def validate(self, input_data):
        """Validate data of type Date."""
        try:
            datetime.strptime(input_data, self.FORMAT_STRING)
        except ValueError:
            return False

        return True


class DecimalValidator(DataValidator):
    """Validates Decimal input data."""

    def validate(self, input_data):
        """Validate data of type Decimal."""
        try:
            float(input_data)
            return True
        except ValueError:
            return False


class XPathValidator(DataValidator):
    """Validates XPATH data provided for parsing XML documents."""

    def validate(self, input_xpath):
        """Validate an XPATH statement."""
        element = XML('<xml></xml>')

        try:
            element.find(input_xpath)
        except Exception:
            return False

        return True


class StringValidator(DataValidator):
    """Validate string data provided by input file."""

    def validate(self, input_string):
        """Validate an individual string."""
        return len(input_string) >= 0


def validate_tuple_data(all_tuples, mapping_configuration):
    """Validate the data in a series of tuples according to the mapping configuration types."""
    for single_tuple in all_tuples:
        result = validate_single_tuple(single_tuple, mapping_configuration)
        if not result:
            return False

    return True


def validate_single_tuple(single_tuple, mapping_configuration):
    """Confirm the provided tuple has data compatible with types specified by mapping config."""
    columns = mapping_configuration.get('columns')
    for count in range(len(single_tuple)):
        for column in columns:
            if column.get('inputIndex') == count:
                if not validate_data(single_tuple[count], column.get('type')):
                    return False
                break

    # All parts of the tuple validated successfully
    return True


def validate_data(tuple_part, data_type):
    """Evaluate the validity of data provided by its given type."""
    if data_type == 'Integer':
        return IntegerValidator().validate(tuple_part)
    elif data_type == 'String':
        return StringValidator().validate(tuple_part)
    elif data_type == 'Date':
        return DateValidator().validate(tuple_part)
    elif data_type == 'Decimal':
        return DecimalValidator().validate(tuple_part)
    else:
        # Data type unknown
        logger.error('Unknown data type provided in mapping config')
        return False

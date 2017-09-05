import argparse
import logging

from p5000.p5000 import load_data

logger = logging.getLogger()

if __name__ == '__main__':
    print('Processor Starting Up')

    parser = argparse.ArgumentParser(prog='p5000',
                                     description='Load data into a database table '
                                                 'based on mapping parameters.')
    parser.add_argument('-i', nargs=1, help='path to an input file', required=True,
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('-m', nargs=1, help='path to the mapping json', required=True,
                        type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('-t', nargs=1, help='the name of the destination table', required=True,
                        type=str)
    parser.add_argument('-c', nargs=1, help='path to the configuration file', required=True,
                        type=argparse.FileType('r', encoding='UTF-8'))

    args = parser.parse_args()
    dict_view = vars(args)

    file_path = dict_view['i'][0].name
    mapping_file = dict_view['m'][0].name
    destination_table = dict_view['t'][0]
    config_file = dict_view['c'][0].name

    print('Input file is {}'.format(file_path))
    print('Mapping configuration is {}'.format(mapping_file))
    print('Destination table is {}'.format(destination_table))
    print('Configuration file is {}'.format(config_file))

    try:
        load_data(file_path, mapping_file, destination_table, config_file)
    except Exception as e:
        logger.error('ERROR: %s', e)
        exit(1)

    print('Processing Completed.')
    exit(0)

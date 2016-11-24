# USAGE
# python3 run.py input1.txt input2.txt output.txt

""" TODO:
# Change syntax based on file_parser modifications
# Add try/catch here
"""

import sys
from file_parser import file_parse
from transition_and_emission import *
# from baseline_system import *


def getScores(outfile_generated, outfile_given):
    # DO THINGS
        return None
if __name__ == '__main__':
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    outfile = sys.argv[3]

    print(train_filename, test_filename, outfile)

    train_parsed_file = file_parse(train_filename, True)
    train_X = train_parsed_file[0]
    train_Y = train_parsed_file[1]

    test_X = file_parse(test_filename, False)

    # next, pass train_X, train_Y, test_X to part_2_project functions
    print(getTag(test_X, train_X, train_Y))

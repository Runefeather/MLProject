# USAGE
# python3 run.py input1.txt input2.txt output.txt

""" TODO:
# Add try/catch here
"""

import sys
from file_parser import file_parse
from transition_and_emission import *
from viterbi import *
# from baseline_system import *


def getScores(outfile_generated, outfile_given):
    # DO THINGS
        return None
if __name__ == '__main__':
    train_filename = sys.argv[1]
    test_filename = sys.argv[2]
    outfile = sys.argv[3]
    function = sys.argv[4]

    print(train_filename, test_filename, outfile)

    train_parsed_file = file_parse(train_filename, True)
    train_X = train_parsed_file[0]
    train_Y = train_parsed_file[1]

    test_X = file_parse(test_filename, False)

    if(function == 'getTags'):
        # next, pass train_X, train_Y, test_X to part_2_project functions
        tags = getTag(test_X, train_X, train_Y)
                
        f = open(outfile,'w')
        for i in range(0, len(test_X)):
            for j in range(0, len(test_X[i])):
                towrite = str(test_X[i][j]) + " " + str(tags[test_X[i][j]])
                f.write(towrite+'\n')
            f.write('\n') 
        f.close() 

    if(function == 'viterbi'):
        # next, pass train_X, train_Y, test_X to part_2_project functions
        # test_Y = viterbi(test_X, train_X, train_Y)

        f = open(outfile,'w')
        for i in range(0, len(test_X)):
            print(test_X[i])
            print("Writing one sentence, " + str(len(test_X)-i) + " to go.")
            viterbi_sentence = viterbi(train_X, train_Y, test_X, test_X[i], len(test_X[i]))
            # print("viterbi_sentence: " + str(len(viterbi_sentence)) + ", X_test: " + str(len(test_X[i])) )
            for j in range(0, len(test_X[i])):
                towrite = str(test_X[i][j]) + " " + str(viterbi_sentence[j])
                # print("writing 1 sentence")
                f.write(towrite+'\n') 
            f.write('\n')
        f.close() 


    # unique = getUnique(train_Y)
    # for i in range(0, len(unique)):
        # print("Yi: " + str(unique[i]) + ", count: " + str(1/(countY(train_Y, unique[i]) + 1)))
        # for j in range(0, len(unique)):
        #     print("Yi: " +str(unique[i]) + ", Yj: " + str(unique[j]) + ", transition params: " + str(transitionParameter(train_Y, unique[i], unique[j])))
# USAGE
# python3 run.py input1.txt-train input2.txt-test output.txt function

""" TODO:
# Add try/catch here
"""

import sys
from file_parser import file_parse
from transition_and_emission import *
from viterbi import *
from viterbi_p4_v3 import *
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
        tags = getTag(test_X, train_X, train_Y)
                
        f = open(outfile,'w')
        for i in range(0, len(test_X)):
            for j in range(0, len(test_X[i])):
                towrite = str(test_X[i][j]) + " " + str(tags[test_X[i][j]])
                f.write(towrite+'\n')
            f.write('\n') 
        f.close() 

    if(function == 'viterbi'):
        f = open(outfile,'w')
        print("generating tables..")
        EMISSION = emissionTable(train_X, train_Y, test_X)
        print("emission done")
        TRANSITION = transitionTable(train_Y)
        print("transition done")
        unique_tags = getUniqueY(train_Y)
        print("unique tags gotten from text")
        print("All pre-requisites done, now running viterbi")
        for i in range(0, len(test_X)):
            # print(test_X[i])
            print("Writing one sentence, " + str(len(test_X)-i) + " to go.")
            viterbi_sentence = viterbi(test_X[i], len(test_X[i]), TRANSITION, EMISSION, unique_tags)
            for j in range(0, len(test_X[i])):
                towrite = str(test_X[i][j]) + " " + str(viterbi_sentence[j])
                f.write(towrite+'\n') 
            f.write('\n')
        f.close() 

    if(function == 'viterbi_topk'):
        f = open(outfile,'w')
        print("generating tables..")
        EMISSION = emissionTable(train_X, train_Y, test_X)
        print("emission done")
        TRANSITION = transitionTable(train_Y)
        print("transition done")
        unique_tags = getUniqueY(train_Y)
        print("unique tags gotten from text")
        print("All pre-requisites done, now running viterbi")
        for i in range(0, len(test_X)):
            # print(test_X[i])
            print("Writing one sentence, " + str(len(test_X)-i) + " to go.")
            viterbi_sentence = viterbiTopK(test_X[i], len(test_X[i]), TRANSITION, EMISSION, unique_tags, 5)[4][1]
            for j in range(0, len(test_X[i])):
                towrite = str(test_X[i][j]) + " " + str(viterbi_sentence[j])
                f.write(towrite+'\n') 
            f.write('\n')
        f.close() 










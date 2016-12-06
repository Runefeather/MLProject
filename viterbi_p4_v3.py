# TODO: 
# ADD LOG FUNCTIONS


import copy
from transition_and_emission import *

# for one sentence
def viterbiTopK(sentence, N, TRANSITION_TABLE, EMISSION_TABLE, unique_tags, topK):

    # {1: key, 2: key, ......, N+1: key}
    trellis = dict.fromkeys(list(range(1, N+2))) 
    # Excluding start state 
    for k in range(1, N+1):
        trellis[k] = dict.fromkeys(unique_tags)

        # for the first layer, prev state= pi(0, S)
        # no topk here
        if k == 1:
            word_to_emit = sentence[k-1]
            for tag in unique_tags:
                # every tag has a list of (values, prev states) associated with it. This is layer 1, so list len is 1
                trellis[k][tag] = [(1*EMISSION_TABLE[(word_to_emit, tag)]*TRANSITION_TABLE[('START', tag)], ['START', tag])]

        # for everything else
        # yes topk here 
        else:
            word_to_emit = sentence[k-1]
            for tag in unique_tags:
                possible_tags = dict.fromkeys(unique_tags)
                for prev_tag in unique_tags:
                    possible_tags[prev_tag] = []
                    for u in range(len(trellis[k-1][prev_tag])):
                        new_seq = copy.deepcopy(trellis[k-1][prev_tag][u][1])
                        new_seq.append(tag)
                        # print((trellis[k-1][prev_tag][u][0]*EMISSION_TABLE[(word_to_emit, tag)]*TRANSITION_TABLE[(prev_tag, tag)], new_seq))
                        possible_tags[prev_tag].append((trellis[k-1][prev_tag][u][0]*EMISSION_TABLE[(word_to_emit, tag)]*TRANSITION_TABLE[(prev_tag, tag)], new_seq))
                # print("POSSIBLE TAGS: " + str(possible_tags))
                possible_tag_values = [possible_tags[v][0] for v in possible_tags.keys()]
                top_k = sorted(possible_tag_values, reverse=True)[:topK]
                # print("TOP K: " + str(top_k))
                # trellis[k][tag] = (max(possible_tags.values()), list(possible_tags.keys())[list(possible_tags.values()).index(max(possible_tags.values()))])
                trellis[k][tag] = top_k
        # print("trellis: " + str(trellis[k]))
        # print("---------------------------------------------")
        # print("---------------------------------------------")

    
    # stop case
    trellis[N+1] = {'STOP' : None}
    possible_tags = dict.fromkeys(unique_tags)

    for tag in unique_tags:
        possible_tags[tag] = []
        for u in range(len(trellis[N][tag])):
            new_seq = copy.deepcopy(trellis[N][tag][u][1])
            new_seq.append('STOP')
            possible_tags[tag].append((trellis[N][tag][u][0]*TRANSITION_TABLE[(tag, 'STOP')], new_seq))
        # print(possible_tags)
    possible_tag_values = [possible_tags[v][0] for v in possible_tags.keys()]
    top_k = sorted(possible_tag_values, reverse=True)[:topK]
    trellis[N+1]['STOP'] = top_k

    return(trellis[N+1]['STOP'])



# TEST CASES:
# X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
# Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
# X_test = [["the", "cat", "cried", "over", "the", "milk"], ["the", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
# -----------------------------------------------------------------------------------------
X = [["b", "c", "a", "b"], ["a", "b", "a"], ["b", "c", "a", "b", "c"], ["c", "b", "a"]]
Y = [["X", "Y", "Z", "X"], ["X", "Z", "Y"], ["Z", "Y", "X", "Z", "Y"], ["Z", "X", "Y"]]
X_test = [["b", "b"]]
EMISSION = emissionTable(X, Y, X_test)
TRANSITION = transitionTable(Y)
unique_tags = getUniqueY(Y)
# print(EMISSION)
# print(TRANSITION)
print(viterbiTopK(X_test[0], len(X_test[0]), TRANSITION, EMISSION, unique_tags, 2))
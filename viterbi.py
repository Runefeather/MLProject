from transition_and_emission import *

# PART 3
# ----------------------------------------------------
# Viterbi algorithm 

# FOR ONE SENTENCE YA
# X_test is entire list of sentences
# N is number of words in 1 sentence
# sentence is sentence
# sentence[k-1] is word at pos k-1 in THAT PARTICULAR SENTENCE
def viterbi(X, Y, X_test, sentence, N):
    if(sentence == []):
        return "NULL"
    unique_tags = getUniqueY(Y)
    trellis = dict.fromkeys(list(range(1, N+2)))
    # 1 to 
    for k in range(1, N+1):
        trellis[k] = dict.fromkeys(unique_tags)

        # for the first layer, the pi(k-1, v) is the start state.
        if k == 1:
            word_to_emit = sentence[k-1]
            for tag in unique_tags:
                trellis[k][tag] = (1*emissionParameter(X, Y, word_to_emit, tag)*transitionParameter(Y, 'START', tag), 'START')
        
        # for everything else
        else:
            word_to_emit = sentence[k-1]
            for tag in unique_tags:
                possible_tags = dict.fromkeys(unique_tags)
           
                for prev_tag in unique_tags:
                    possible_tags[prev_tag] = trellis[k-1][prev_tag][0]*emissionParameter(X, Y, word_to_emit, tag)*transitionParameter(Y, prev_tag, tag)
                trellis[k][tag] = (max(possible_tags.values()), list(possible_tags.keys())[list(possible_tags.values()).index(max(possible_tags.values()))])
        # print("trellis: " + str(trellis[k]))
    
    # stop case
    possible_tags = dict.fromkeys(unique_tags)
    for tag in unique_tags:
        possible_tags[tag] = trellis[N][tag][0]*transitionParameter(Y, tag, 'STOP')
    trellis[N+1] = {'STOP': (max(possible_tags.values()), list(possible_tags.keys())[list(possible_tags.values()).index(max(possible_tags.values()))])}

    return backtrack(trellis) 
    

def backtrack(trellis):
    N = len(trellis.keys())
    path = [0]*N

    path[N-1] = 'STOP'

    for i in range(0, (N-1)):
        path[N-i-2] = trellis[N-i][path[N-1-i]][1]
    return path



# TEST CASES:
# X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
# Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
# X_Test = [["the", "cat", "cried", "over", "the", "milk"], ["the", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
# print(viterbi(X, Y, X_Test, X_Test[0], len(X_Test[0])))
# -----------------------------------------------------------------------------------------
# X = [["b", "c", "a", "b"], ["a", "b", "a"], ["b", "c", "a", "b", "c"], ["c", "b", "a"]]
# Y = [["X", "Y", "Z", "X"], ["X", "Z", "Y"], ["Z", "Y", "X", "Z", "Y"], ["Z", "X", "Y"]]
# X_test = [["b", "b"]]
# print(viterbi(X, Y, X_test, X_test[0], len(X_test[0])))

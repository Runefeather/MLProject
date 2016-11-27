from transition_and_emission import *
# FIX THIS 
# -------------------------------------------------------------------------------------------
# PART 3
# Viterbi algorithm

# neighbours for one layer is the previous layer
# here i is the previous layer
def getNeighbours(pathweights, i):
    neighbours = {}
    for key in pathweights[i].keys():
        # print(pathweights[key])
        # print(key[0], i)
        if(key[0] == (i)):
            neighbours[key[1]] = pathweights[i].get(key)[0]
    return neighbours

def viterbi(X_test, X, Y):
    nodes = getUnique(Y)
    # for each sentence
    final_weights = [list() for x in range(len(X_test))]
    for i in range(len(X_test)):
        # words in one sentence
        num_words = len(X_test[i])
        print("number of words: " + str(num_words))
        # number of states at each layer
        unique_states = len(nodes)
        # total steps = start + words + stop
        num_steps = num_words + 2
        pathweights = [dict() for x in range(num_steps)]

        # now iterating over words in sentence:
        for k in range(num_steps):
            # if k is 0, start state
            if k == 0:
                pathweights[0] = {(k, 'START') : (1, None)}
                # print(pathweights[k])
            elif k <= num_words:
                # print("k is: " + str(k))
                dictionary_weights = {}
                # neighbours is previous layer
                neighbours = getNeighbours(pathweights, k-1)
                for node in nodes:
                    # print("node: " + str(node))
                    # print("Xtest: " + str(X_test[i][k-1]))
                    # print(neighbours)
                    # viterbi for words in sentence
                    rec = forwardRecursion(X, Y, k, node, X_test[i][k-1], neighbours)
                    dictionary_weights[(k, node)] = (rec[0], rec[1])
                pathweights[k] = dictionary_weights
                # print(pathweights)
                print("----------------------------")
            else:
                # stop case
                neighbours = getNeighbours(pathweights, k-1)
                # print("last neighbours: " + str(neighbours))
                final = finalStep(Y, nodes, neighbours)
                pathweights[k] = {(k, 'STOP') : (final[0], final[1])}
        final_weights[i] = pathweights
    return final_weights


def getFullPath(final_weights):
    full_path = [list() for x in range(len(final_weights))]
    for pathweights in final_weights: 
        num_steps = len(pathweights)
        full_path_sentence = [0]*num_steps
        full_path_sentence[0] = 'START'
        full_path_sentence[num_steps-1] = 'STOP'
        last_tag = pathweights[num_steps-1].get((num_steps-1, 'STOP'))[1]
        full_path_sentence[num_steps-2] = last_tag
        for i in range(0, num_steps-2):
            # print("i: " + str(i) + ", pw: " + str(pathweights[num_steps-i-1]) + ", last tag: " + str(last_tag))
            full_path_sentence[num_steps-3-i] = pathweights[num_steps-2-i].get((num_steps-2-i, last_tag))[1]
            # print("next tag: " + str(pathweights[num_steps-2-i].get((num_steps-2-i, last_tag))[1]))
            last_tag = full_path_sentence[num_steps-3-i]
        full_path.append(full_path_sentence)
    return full_path


def finalStep(Y, nodes, neighbours):
    list_of_values = {}
    for node in nodes:
        for key in neighbours.keys():
            if node == key:
                list_of_values[node] = neighbours[key]*transitionParameter(Y, node, 'STOP')
    max_val = max(list(list_of_values.values()))
    max_node = list(list_of_values.keys())[list(list_of_values.values()).index(max_val)]
    return(max_val, max_node)


# pi(k, v) = max over u {pi(k-1, u)*transition(u,v)*emission(xk. v)}
def forwardRecursion(X, Y, k, v, xk, neighbours):
    # print(neighbours)
    # neighbours: {node: value}  
    emission = emissionParameter(X, Y, xk, v)
    list_of_values = {}
    for key in neighbours.keys():
        node = key
        value = neighbours.get(key)
        # print(node, value)
        transition = transitionParameter(Y, node, v)
        # print("val, transition, emission: " + str(value) + " " + str(transition) + " " + str(emission))
        list_of_values[key] = value*transition*emission
        # print(" list_of_values[key] = " + str(list_of_values[key]))

    # print("list of values: " + str(list_of_values))
    max_val = max(list(list_of_values.values()))
    max_node = list(list_of_values.keys())[list(list_of_values.values()).index(max_val)]
    return(max_val, max_node)


X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
X_test = [["the", "cat", "cried", "over", "the", "milk"], ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
# X = [["b", "c", "a", "b"], ["a", "b", "a"], ["b", "c", "a", "b", "c"], ["c", "b", "a"]]
# Y = [["X", "Y", "Z", "X"], ["X", "Z", "Y"], ["Z", "Y", "X", "Z", "Y"], ["Z", "X", "Y"]]
# X_test = [["b", "b"]]

viterbi = viterbi(X_test, X, Y)
print(viterbi)
print("# --------------------------------------------------")
print(getFullPath(viterbi))
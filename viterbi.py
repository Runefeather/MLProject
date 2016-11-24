from transition_and_emission import *
# FIX THIS 
# -------------------------------------------------------------------------------------------
# PART 3
# Viterbi algorithm
# figure out START and STOP conventions. Is this in data?

""" 
parameters: X(x_train)
			Y(y_train)
			u(dictionary of {tag:weight} for k-1 layer)
			k(layer we are looking at)
			v(the tag we want)
			xk(the word/observation we want)
"""
def viterbi(X, Y, u, k, v, xk):
	# base case- pi(0, S) = 1. 
	if k == 0 and (v == 'START' or v == '0'):
		return 1
	# base case- pi(0, any_other_tag) = 0
	elif k == 0 and (v != 'START' or v != '0'):
		return 0
	# this should not happen, but for little-remaining-sanity's sake and all that
	elif k != 0 and v == 'START':
		return 0
	else:
		# pi(k,v) = max(u) {pi(k-1, u)*transition(u, v)*emission(v, xk)}
		possible_weights = {}
		for tag in u.keys():
			# print(transitionParameter(Y, tag, str(v)))
			# print(emissionParameter(X, Y, str(xk), str(v)))
			print(tag, v)
			possible_weights[tag] = u[tag]*transitionParameter(Y, tag, v)*emissionParameter(X, Y, str(xk), str(v))

		# now, max of all possible weights
		max_weight = max(list(possible_weights.values()))
		# ...and the corresponding key value
		max_node = list(possible_weights.keys())[list(possible_weights.values()).index(max_weight)]
		return (max_node, max_weight)

# * Forward case
# * go through all sentences in test set, give tags to words
def forwardCase(X_test, X, Y):
	# number of nodes at each layer
	nodes = getUnique(Y)

	pathweights = [0]*(len(X_test)+2)
	pathweights[0] = {"START":1}

	for i in range(0, len(X_test)):
		# number of layers = number of words in sentence
		layers = len(X_test[i])
		
		# dictionary of {word:(prev node, weight)}
		word_weights = {}
		# weights of different nodes for one word
		node_weights = [0]*len(nodes)

		# now to do the viterbi for each word in sentence..
		for j in range(0, len(X_test[i])):
			# calculating weights for each tag: 
			for k in range(0, len(nodes)):
				# print(nodes[k])
				node_weights[k] = viterbi(X, Y, pathweights[i], j, nodes[k], X_test[i][j])
			word_weights[X_test[i][j]] = node_weights
		pathweights[i+1] = word_weights
		print(pathweights)
	return pathweights


X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
X_test = [["the", "cat", "cried", "over", "the", "milk"], ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
print(forwardCase(X_test, X, Y))
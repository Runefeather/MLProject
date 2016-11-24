from transition_and_emission import *

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
	elif k == 0 and (v != 'START' or v =! '0'):
		return 0
	# this should not happen, but for little-remaining-sanity's sake and all that
	elif k != 0 and v == S:
		return 0
	else:
		# pi(k,v) = max(u) {pi(k-1, u)*transition(u, v)*emission(v, xk)}
		possible_weights = {}
		for tag in u.keys():
			possible_weights[tag] = u[tag]*transitionParameter(Y, tag, v)*emissionParameter(X, Y, xk, v)

		# now, max of all possible weights
		max_weight = max(list(possible_weights.values()))
		# ...and the corresponding key value
		max_node = list(possible_weights.keys())[list(possible_weights.values()).index(max_weight)]
		return {max_node:max_weight}

# * Forward case
# * go through all sentences in test set, give tags to words
def forwardCase(X_test, X, Y):
	# number of nodes at each layer
	nodes = getUnique(Y)

	pathweights = [0]*len(X_test)

	for i in range(0, len(X_test)):
		# number of layers = number of words in sentence
		layers = len(X_test[i])
		
		# now to do the viterbi for each word in sentence..
		

# Assume that training data is split over two lists: X and Y
# where every X[i] contains words in one sentence
# and Y[i] contains respective tags for that sentence
# which means, X[i][j] is a word, and Y[i][j] is corresponding tag


# counts number of times y appears in Y
def countY(Y, tag):
    total_Y = 0
    for tags_for_sentence in Y:
        total_Y += tags_for_sentence.count(tag)
    return total_Y

# check if x is in X
def checkX(X, word):
    for sentence in X:
        if word in sentence:
            return True

# get all unique tags in Y
def getUnique(Y):
    return list(set(x for l in Y for x in l))

# get emission estimates
def emissionEstimate(X, Y, x, y):
    count_YX = 0
    # assume that training set is properly formed
    # which means len(X) == len(Y)
    # and len(X[i]) == len(Y[i]) for all i
    # I'm looking at you, Arjun.
    length = len(X)
    # if x is in training set
    if checkX(X,x):
        for i in range(0, length):
            for j in range(0, len(X[i])):
                if Y[i][j] == y and X[i][j] == x:
                    count_YX += 1
        return (count_YX/countY(Y, y))
    # if not
    else:
        return (1/(countY(Y, y) + 1))

# Implement a simple sentiment analysis system that produces the tag
# y∗ = arg max e(x|y)
# for each word x in the sequence
# X, Y
def getTag(X, Y):
    tags_for_X = list(X)
    unique_tags = getUnique(Y)
    for sentence in X:
        for word in sentence:
            possible_Y = [0]*len(unique_tags)
            for i in range(0, len(unique_tags)):
                possible_Y[i] = emissionEstimate(X, Y, word, unique_tags[i])
            tags_for_X[X.index(sentence)][sentence.index(word)] = unique_tags[possible_Y.index(max(possible_Y))]
    return tags_for_X


# test cases
X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
print("for word in training set:" + str(emissionEstimate(X, Y, "the", "D")))
print("for word in training set:" + str(emissionEstimate(X, Y, "the", "P")))
# this is weird. must email LiHao
print(getTag(X,Y))


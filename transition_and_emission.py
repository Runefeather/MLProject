# Assume that training data is split over two lists: X and Y
# where every X[i] contains words in one sentence
# and Y[i] contains respective tags for that sentence
# which means, X[i][j] is a word, and Y[i][j] is corresponding tag


# HELPER FUNCTIONS
# -------------------------------------
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

# count pattern of tags
# ASSUMING THAT START = 0, STOP = 9
def countPattern(Y, pattern):
    all_Y = ''
    for y in Y:
        all_Y += '0'
        all_Y += ''.join(map(str,y))
        all_Y += '9'
    # print(all_Y)
    return all_Y.count(pattern)

# -------------------------------------------------------------------------------------------
# PART 2


# EMISSION PARAMETERS FOR ONE (xi, yi)
# -------------------------------------
# get emission estimates
def emissionParameter(X, Y, x, y):
    count_YX = 0
    # assume that training set is properly formed
    # which means len(X) == len(Y)
    # and len(X[i]) == len(Y[i]) for all i
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

# GET TAGS FOR ALL SENTENCES USING EMISSION PARAMETERS
# -------------------------------------
# Implement a simple sentiment analysis system that produces the tag
# y∗ = arg max e(x|y)
# for each word x in the sequence
# X, Y
def getTag(X_Test, X, Y):
    tags_for_X = list(X_Test)    
    unique_tags = getUnique(Y)
    print(unique_tags)
    print("Getting tags..   ")
    # print(len(X_Test))
    counter = 0
    for sentence in X_Test:
        counter += 1
        for word in sentence:
            possible_Y = [0]*len(unique_tags)
            for i in range(0, len(unique_tags)):
                possible_Y[i] = emissionParameter(X, Y, word, unique_tags[i])
            tags_for_X[X_Test.index(sentence)][sentence.index(word)] = unique_tags[possible_Y.index(max(possible_Y))]
        print("1 sentence down, " + str(len(X_Test) - counter)+ " to go")
    print("Done!")
    return tags_for_X

# -------------------------------------------------------------------------------------------
# PART 3


# TRANSITION PARAMETERS FOR ONE (yi-1, yi)
# -------------------------------------
# transition parameter q(yi|yi-1) = count(yi-1, yi)/count(yi-1)
def transitionParameter(Y, yi_minus_one, yi):
    # print(yi_minus_one, yi)
    if yi_minus_one == 'START':
        pattern = '0' + yi
        count_yi_minus_one = len(Y)

    elif yi == 'STOP':
        pattern = yi_minus_one + '9'
        count_yi_minus_one = countY(Y, yi_minus_one)

    else:
        pattern = yi_minus_one + yi
        count_yi_minus_one = countY(Y, yi_minus_one)

    transiton_count = countPattern(Y, pattern) 
    return transiton_count/count_yi_minus_one


# test cases- THESE ARE BAD ONES, BUT THEY CHECK FUNCTIONALITY, SO OH WELL
X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
# print("for word in training set:" + str(emissionParameter(X, Y, "the", "D")))
# print("for word in training set:" + str(emissionParameter(X, Y, "the", "P")))
X_Test = [["the", "cat", "cried", "over", "the", "milk"], ["The", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]
# print(getTag(X_Test, X, Y))
# print("transition params: " + str(transitionParameter(Y, 'START', 'D')))
# print("transition params: " + str(transitionParameter(Y, 'N', 'STOP')))
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
def getUniqueY(Y):
    return list(set(y for l in Y for y in l))

# get all unique words in X
def getUniqueX(X):
    return list(set(x for l in X for x in l))

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
        return (count_YX/(countY(Y, y) + 1))
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
    # dictionary of {word : tag}
    tags_for_X = {}    
    # unique tags
    unique_tags = getUniqueY(Y)
    # unique words, because here, order does not matter
    unique_words = getUniqueX(X_Test)
    print("Getting tags..   ")
    counter = 0

    for word in unique_words:
        counter += 1
        possible_Y = {}
        for tag in unique_tags:
            possible_Y[tag] = emissionParameter(X, Y, word, tag)
        # print("word: " + str(word) + ", possible y: " + str(possible_Y))
        max_val = max(possible_Y.values())
        # print("max: " + str(max(possible_Y.values())))    
        tags_for_X[word] = list(possible_Y.keys())[list(possible_Y.values()).index(max_val)]
        print("1 word down, " + str(len(unique_words) - counter) + " to go")
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
# X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
# Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
# X_Test = [["the", "cat", "cried", "over", "the", "milk"], ["the", "Spoon", "and", "fork", "ran", "away", "from", "the", "knife"]]


# print(getUniqueX(X_Test))
# print("for word in training set:" + str(emissionParameter(X, Y, "the", "D")))
# print("for word in training set:" + str(emissionParameter(X, Y, "the", "P")))
# print(getTag(X_Test, X, Y))
# print("transition params: " + str(transitionParameter(Y, 'START', 'D')))
# print("transition params: " + str(transitionParameter(Y, 'N', 'STOP')))

# Assume that training data is split over two lists: X and Y 
# where every X[i] contains words in one sentence
# and Y[i] contains respective tags for that sentence
# which means, X[i][j] is a word, and Y[i][j] is corresponding tag

def emission_estimates(X, Y, x, y):
    countYX = 0
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
                    countYX += 1
        return (countYX/countY(Y, y))
    # if not
    else:
        return (1/countY(Y, y))

# counts number of times y appears in Y
def countY(Y, y):
    totalY = 0
    for yi in Y:
        totalY += yi.count(y)
    return totalY

# check if x is in X
def checkX(X, x):
    for xi in X:
        if x in xi:
            return True

# test cases
X = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "dish", "ran", "away", "with", "the", "spoon"]]
Y = [["D", "N", "V", "P", "D", "N"], ["D", "N", "V", "A", "P", "D", "N"]]
print("for word in training set:" + str(emission_estimates(X, Y, "the", "D")))
print("for word in training set:" + str(emission_estimates(X, Y, "the", "P")))
print("for word not in training set:" + str(emission_estimates(X, Y, "bull", "D")))






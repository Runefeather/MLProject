# author: arjun brar
# parses input file to [[sentence], [sentence], [sentence]] and [[tag], [tag], [tag]]
# return it in tuple format of (X, Y)

def file_parse(filename):
    # Open the file to read
    f = open(filename, "r")

    #initializing the return variables
    X = []
    Y = []

    #initializing the temporary variables
    wordL = []
    tagL = []

    #going over every line in the file
    for line in f:

        #repr to get the \n char, stripping the " and '.
        item = repr(line.strip("\n")).strip("'").strip('"')

        #checking for new sentence
        if len(item) != 0:
            #splitting the line into word and tag
            word, tag = item.split(" ")
            #appending word and tag into temp variables
            wordL.append(word)
            tagL.append(tag)
        else:
            #appending temp variables to X and Y
            X.append(wordL)
            Y.append(tagL)

            #reinitializing temp variables
            wordL = []
            tagL = []

    # performing sanity check for X and Y
    for i in range(len(X)):
        if len(X[i]) != len(Y[i]):
            print "issue at sentence", str(i)

    print "Done"
    return X, Y

print file_parse("train")
# author: arjun brar
# arguments: name of the file to be parsed, and a true/false for whether it is in training mode or not.
# parses input file to [[sentence], [sentence], [sentence]] and [[tag], [tag], [tag]]
# return it in tuple format of (X, Y)

DEBUG=False

def file_parse(filename, training):
    # Open the file to read
    f = open(filename, "r")

    if training:
        #initializing the return variables
        X = []
        Y = []

        #initializing the temporary variables
        wordL = []
        tagL = []

        #going over every line in the file
        for line in f:
            #repr to get the \n char, stripping the " and '.
            item = line.strip("\n\r")

            #checking for new sentence
            if len(item) != 0:
                # print(item)
                #splitting the line into word and tag
                word, tag = item.split(" ")

                # debugging stuff
                if DEBUG:
                    print(repr(line.strip("\n\r")).strip("'").strip('"'), len(repr(line.strip("\n\r")).strip("'").strip('"')))
                    print(word)

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

        # performing sanity check for X and Y- added a return so it breaks here
        for i in range(len(X)):
            if len(X[i]) != len(Y[i]):
                print("issue at sentence", str(i))



        return X, Y
    else:
        #initializing the return variables
        X = []

        #initializing the temporary variables
        wordL = []

        #going over every line in the file
        for line in f:
            #repr to get the \n char, stripping the " and '.
            item = line.strip("\n\r")
            
            #checking for new sentence
            if len(item) != 0:
                #splitting the line into word and tag
                word = item

                # debugging stuff
                if DEBUG:
                    print(repr(line.strip("\n\r")).strip("'").strip('"'), len(repr(line.strip("\n\r")).strip("'").strip('"')))
                    print(word)

                #appending word and tag into temp variables
                wordL.append(word)
            else:
                #appending temp variables to X and Y
                X.append(wordL)

                #reinitializing temp variables
                wordL = []

        return X

# Test
# print(file_parse("EN/dev.in", False))

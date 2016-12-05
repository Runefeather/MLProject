"""
Imports necessary for the code
"""
import copy
import collections


"""
Setting up the language and files to use
"""
lang = "EN"
training_file = lang + "/train"
input_file = lang + "/dev.in"
out_file = lang + "/dev.p5_tester.out"


"""
A Bigram Model
"""
class bigram(object):
    def __init__(self):
        ''' initializing the strings for words and tags for curr and prev state '''
        self.priorWord = ''
        self.priorTag = ''
        self.currentWord = ''
        self.currentTag = ''

        ''' initializing the transistion and tuple_emission tuples '''
        self.transition = ()
        self.emission = ()

        ''' initializing the counts for things '''
        self.wordCount = 0.0
        self.tagCount = 0.0
        self.priorTagCount = 0.0
        self.transCount = 0.0
        self.emitCount = 0.0

        ''' initializing list of tags '''
        self.possTags = []

        ''' initializing probabilities '''
        self.transProb = 0.0
        self.emishProb = 0.0
        self.finalProb = 0.0

    def calculate_score(self):
        ''' calculates the score for transistion and tuple_emission '''
        self.transProb = self.transCount/float(self.priorTagCount)
        self.emishProb = self.emitCount/float(self.tagCount)
        self.finalProb = self.transProb * self.emishProb



"""
Class for storing one sentence's information
"""
class sentence(object):
    def __init__(self):
        ''' list of words in sentences'''
        self.bigrams = []
        self.score = 0
        self.max = 0

    def sentScore(self):
        switch = 0
        for gram in self.bigrams:
            if switch == 0:
                self.score = gram.finalProb
                switch = 1
            else:
                self.score = self.score * float(gram.finalProb)



"""
Class for storing information on all sentences
"""
class all_sentences(object):
    def __init__(self):
        ''' initializing list to store all sentences '''
        self.list      = []

        ''' initializing max score of the sentence '''
        self.sentsMax = 0

    def addWord(self,gram):
        for sentence in self.list:
            sentence.bigrams.append(gram)

    def addSentence(self):
        sent = sentence()
        self.list.append(sent)

def main():

    # ok, this is where the magic starts.
    # start by opening the file to train from
    # opening as r since we only need to read - no writing should be done here
    file=open(training_file,'r')

    #list of bigrams for aggregating data
    theBigrams = []

    #dictionairies for counting
    wordDic = collections.defaultdict(int)
    tagDic = collections.defaultdict(int)
    transDic = collections.defaultdict(int)
    emitDic = collections.defaultdict(int)
    possDic1 = collections.defaultdict(list)
    possDic2 = collections.defaultdict(int)

    #last pos -> most likely pos
    lastDic = collections.defaultdict(str)

    #variables to store for the next iteration
    lastWord = ''
    lastTag = ''
    lastTagCount = 0


    #FIRST PASS~~~~~~
    #parsing input data
    #aggregating dictionairies
    file.seek(0)
    for line in file:

        gram = bigram()
        thisLine = line.split()
        listLen = len(thisLine)

        #assign PRIOR word and tag to gram
        gram.priorWord = lastWord
        gram.priorTag = lastTag
        gram.priorTagCount = lastTagCount

        #if the current line contains a word and a tag
        if listLen > 1:

            #assign CURRENT word and tag to gram
            gram.currentWord = thisLine[0]
            gram.currentTag = thisLine[1]

            #and add to dictionairy -> list
            possDic1[gram.currentWord].append(gram.currentTag)

        else:
            gram.currentWord = ''
            gram.currentTag = ''

        #store transition & emission
        gram.transition = (gram.priorTag,gram.currentTag)
        gram.emission = (gram.currentTag,gram.currentWord)

        #increment dictionairies
        transDic[gram.transition] += 1
        emitDic[gram.emission] += 1
        wordDic[gram.currentWord] += 1
        tagDic[gram.currentTag] += 1
        possDic2[gram.currentWord] += 1

        #add the gram to our list
        theBigrams.append(gram)

        #set temp variables for next gram
        lastWord = gram.currentWord
        lastTag = gram.currentTag
        lastTagCount = gram.tagCount


    #Uniqify thingys in possDic1
    for thingy in possDic1:
        possDic1[thingy]=list(set(possDic1[thingy]))

    copyTagDic = copy.deepcopy(tagDic)
    copyTransDic = copy.deepcopy(transDic)

    #lastDic will have tag -> tag+1 in strings
    for tag in copyTagDic:
        lastDic[tag] = ""

    #Counting total transitions from tag
    for trans in transDic:
        copyTagDic[trans[0]] += 1

    #Taking transDic from count to prob
    for trans in transDic:
        copyTransDic[trans] = transDic[trans]/ float(copyTagDic[trans[0]])

    #Setting copyTagDic back to zero
    for tag in copyTagDic:
        copyTagDic[tag] = 0

    #Setting max
    for item in copyTransDic:
        if copyTagDic[item[0]] < copyTransDic[item]:
            copyTagDic[item[0]] = copyTransDic[item]

    #Storing in lastDic
    for item in copyTransDic:
        if copyTagDic[item[0]] == copyTransDic[item]:

            #mapping tag -> tag + 1
            lastDic[item[0]] = item[1]

    gramDic = collections.defaultdict(bigram)

    #COUNTING~~~~~~~~~~~~~
    #We want the data from the dictionairies
    #stored locally with each bigram object
    for item in theBigrams:

        item.wordCount = wordDic[item.currentWord]
        item.tagCount = tagDic[item.currentTag]
        item.priorTagCount = tagDic[item.priorTag]
        item.transCount = transDic[item.transition]

        if item.emission[0] == item.currentTag and item.emission[1] == item.currentWord:
            item.emitCount = emitDic[item.emission]

        item.possTags = possDic1[item.currentWord]

        item.calculate_score()
        gramDic[(item.currentWord,item.currentTag)] = item


    f = open("test.doc", "w")
    f.write(str(gramDic))
    #SECOND PASS~~~~~~~~
    #Building up lists of possible word combinations or "sentences"
    #Computing likelihood of each tag sequence

    file=open(input_file,'r')

    sentsList = []
    newSents = 1
    sentsListNum = 0
    theLastTag = ''
    for word in file:

        wordList = word.split()
        currentTag = ''

        if len(wordList) > 0:
            theWord = wordList[0]
            tags = possDic1[theWord]

            if newSents == 1:
                newSents = 0
                sents = all_sentences()
                sents.addSentence()

            if len(tags) >= 1:

                tagMax = 0
                for tag in tags:
                    gram = gramDic[(theWord,tag)]
                    currentTag = tag

                    if gram.finalProb >= tagMax:
                        tagMax = gram.finalProb

                for tag in tags:
                    gram = gramDic[(theWord,tag)]

                    if gram.finalProb == tagMax:
                        sents.addWord(gram)

            else:
                if len(tags) == 0:
                    gram = bigram()
                    gram.currentWord = theWord
                    gram.currentTag = lastDic[theLastTag]
                    gram.finalProb = .0001
                    gramDic[(gram.currentWord,gram.currentTag)] = gram

                else:
                    gram = gramDic[(theWord,tags[0])]
                    currentTag = tags[0]

                sents.addWord(gram)

        else:
            newSents = 1
            sentsList.append(sents)
            sentsListNum = sentsListNum + 1

        theLastTag = currentTag

    #Find max
    for sents in sentsList:
        for sent in sents.list:
            sent.sentScore()
            if sent.score > sents.sentsMax:
                sents.sentsMax = sent.score


    outfile = open(out_file,"w")

    #Write output
    for sents in sentsList:
        num = 0
        for sent in sents.list:
            if sent.score == sents.sentsMax and num == 0:
                for gram in sent.bigrams:
                    outfile.write(str(gram.currentWord)+" "+str(gram.currentTag)+"\n")
                num += 1
                outfile.write("\n")

if __name__ == "__main__":
    main()
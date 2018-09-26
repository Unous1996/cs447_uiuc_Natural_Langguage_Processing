########################################
## CS447 Natural Language Processing  ##
##           Homework 0               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Read in a text file (consisting of one sentence per line) into a data structure
##
import os.path
import sys
import functools
#----------------------------------------
#  Data input 
#----------------------------------------

# Read a text file into a corpus 
def readFileToCorpus(f):
    """ Reads in the text file f which contains one sentence per line.
    """
    if os.path.isfile(f):
        file = open(f, "r") # open the input file in read-only mode
        i = 0 # this is just a counter to keep track of the sentence numbers
        corpus = [] # this will become a list of sentences
        print("reading file ", f)
        for line in file:
            i += 1
            sentence = line.split()  # split the line into a list of words
            corpus.extend(sentence)  # extend the current list of words with the words in the sentence
            if i % 1000 == 0:
                sys.stderr.write("Reading sentence " + str(i) + "\n") # just a status message: str(i) turns the integer i into a string, so that we can concatenate it
        return corpus
    else:
        print("Error: corpus file ", f, " does not exist")  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
        sys.exit() # exit the script

#-------------------------------------------
# Data output
#-------------------------------------------
# Print out corpus statistics:
def countWords(corpus):
    print("Total number of words in the corpus is:"+str(len(corpus)))
    #print("Your task 1: count the total number of words (tokens) in our corpus")

def getVocab(corpus):

    def compareWords(word1, word2):
        if len(word1) == 0:
            return 1
        if len(word2) == 0:
            return -1
        for i in range(0, min(len(word1), len(word2))):
            if word1[i] > word2[i]:
                return 1
            if word1[i] < word2[i]:
                return -1
        return [-1, 1][len(word1) > len(word2)]

    raw_list = sorted(corpus, key=functools.cmp_to_key(compareWords))
    result_list = []
    prev_item = raw_list[0]
    result_list.append(prev_item)
    for item in raw_list[1:]:
        if item != prev_item:
            result_list.append(item)
        prev_item = item

    return result_list

def printWordFrequencies(index, vocab):
    def printWordFreqCompare(list1, list2):
        if len(list1[1]) < len(list2[1]):
            return 1
        else:
            return -1
    rawlist = []
    for voc in vocab:
        rawlist.append([voc, index[voc]])
    rawlist = sorted(rawlist, key=functools.cmp_to_key(printWordFreqCompare))
    for item in rawlist:
        print("word:"+item[0]+" freq:"+str(len(item[1])))

#
# Print out all occurrences of the word 'word' in the corpus indexed by index
#
def printCorpusConcordance(word, corpus, index):
    for pos in index[word]:
        printConcordance(corpus, pos)

#
#  Print out the concordance of the word at position word_i
#  in sentence sentence, e.g: 
# 
"""
>>> printConcordance(1, ["what's", 'the', 'deal', '?'])
                                  what's    the     deal ?
>>> printConcordance(1,['watch', 'the', 'movie', 'and', '"', 'sorta', '"', 'find', 'out', '.', '.', '.'])
                                   watch    the     movie and " sorta " 
>>> printConcordance(3,['so', 'what', 'are', 'the', 'problems', 'with', 'the', 'movie', '?'])
                             so what are    the     problems with the movie ?     
"""

def printConcordance(corpus, word_i):
    """ print out the five words preceding word,
        the word at position i and the following five words."""
    if word_i < len(corpus):
        start = max(word_i-5, 0)
        end = min(word_i+6, len(corpus))
        left = ' '.join(corpus[start:word_i])
        right = ' '.join(corpus[word_i+1:end])
        print(left.rjust(40), corpus[word_i].center(10), right.ljust(30))

#--------------------------------------------------------------
# Corpus analysis
#--------------------------------------------------------------

#
# Create an index that maps each word to all its positions in the corpus
#
def createCorpusIndex(corpus):
    # we create a dictionary (associative array) that maps words
    # to a list of their positions
    index = {}
    for i in range(len(corpus)):
        word = corpus[i]
        if (word in index):
            index[word] += [i]
        else:
            index[word] = [i]
    return index

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    movieCorpus = readFileToCorpus('movies.txt')
    countWords(movieCorpus)
    movieVocab = getVocab(movieCorpus)
    movieIndex = createCorpusIndex(movieCorpus)
    printWordFrequencies(movieIndex, movieVocab)
    printCorpusConcordance("the", movieCorpus, movieIndex)


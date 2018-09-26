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

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
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
            sentence = line.split() # split the line into a list of words
            corpus.append(sentence) # append this list as an element to the list of sentences
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
# - how many sentences?
# - how many word tokens?
def printStats(corpus):
    total_tokens = 0
    for sent in corpus:
        total_tokens += len(sent)
    print("Total number of sentences is:", len(corpus))
    print("Total number of word tokens is:", total_tokens)
#   print("Your task 1: count the total number of sentences and words (tokens) in our corpus")
#
#
#

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

    total_list = []
    for sent in corpus:
        total_list.extend(sent)

    sorted_list = sorted(total_list, key=functools.cmp_to_key(compareWords))
    result_list = []
    prev_item = sorted_list[0]
    result_list.append(prev_item)
    for item in sorted_list[1:]:
        if item != prev_item:
            result_list.append(item)
        prev_item = item
    return result_list

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

def printConcordance(sentence, word_i):
    """ print out the five words preceding word,
        the word at position i and the folllowing five words."""
    if word_i < len(sentence):
        start = max(word_i-5, 0)
        end = min(word_i+6, len(sentence))
        left = ' '.join(sentence[start:word_i])
        right = ' '.join(sentence[word_i+1:end])
        print(left.rjust(40), sentence[word_i].center(10), right.ljust(30))

#--------------------------------------------------------------
# Corpus analysis (tokens as class)
#--------------------------------------------------------------

# We use the class Token to point to individual tokens (words) in the corpus.
class Token:
    def __init__(self, s, w): # we need to initialize each instance of Token:
        self.sentence = s # sentence is the index of the sentence (in the corpus)
        self.word = w # word is the index of the word (in the sentence)

#--------------------------------------------------------------
# Corpus analysis (tokens as tuple (i, j))
#--------------------------------------------------------------

#
# Create an index that maps each word to all its positions in the corpus
# (tokens are encoded as a tuple)
#
def createCorpusIndex_TupleVersion(corpus):
    index = {}
    for i in range(0,len(corpus)):
        for j in range(0, len(corpus[i])):
            word = corpus[i][j]
            if word in index:
                index[word] += [(i,j)]
            else:
                index[word] = [(i,j)]
    return index

def printWordFrequencies_TupleVersion(index, vocab):

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

#    print("Your task 4: print out a list of all the words that occur in the corpus and their frequencies, using the tuple-based index")
#    print("            This list should be sorted by word frequencies in descending order (most frequent word first)")

#
# Print out all occurrences of the specified word in the corpus indexed by index
# (tokens are encoded as a tuple)
#
def printCorpusConcordance_TupleVersion(word, corpus, index):
    for pos in index[word]:
        printConcordance(corpus[pos[0]], pos[1])

#
# Create an index that maps each word to all its positions in the corpus
# (tokens are encoded as a tuple)
#
def createCorpusIndex_ClassVersion(corpus):
    index = {}
    for i in range(0,len(corpus)):
        for j in range(0, len(corpus[i])):
            word = corpus[i][j]
            if word in index:
                index[word] += [Token(i, j)]
            else:
                index[word] = [Token(i, j)]
    return index

#
# Prints out all words sorted by their frequency, in descending order
#
def printWordFrequencies_ClassVersion(index, vocab):
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
#    print("Your task 7: print out a list of all the words that occur in the corpus and their frequencies, using the class-based index")
#    print("            This list should be sorted by word frequencies in descending order (most frequent word first)")

#
# Print out all occurrences of the word 'word' in the corpus indexed by index 
# (tokens are encoded as a class)
#
def printCorpusConcordance_ClassVersion(word, corpus, index):
    for pos in index[word]:
        printConcordance(corpus[pos.sentence], pos.word)
    print("Your task 8: using the class version of the index, print out the concordances")

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    movieCorpus = readFileToCorpus('movies.txt')
    printStats(movieCorpus)
    movieVocab = getVocab(movieCorpus)
    movieIndexTuples = createCorpusIndex_TupleVersion(movieCorpus)
    printWordFrequencies_TupleVersion(movieIndexTuples, movieVocab)
    printCorpusConcordance_TupleVersion("the", movieCorpus, movieIndexTuples)
    movieIndexClass = createCorpusIndex_ClassVersion(movieCorpus)
    printWordFrequencies_ClassVersion(movieIndexTuples, movieVocab)
    printCorpusConcordance_ClassVersion("the", movieCorpus, movieIndexClass)

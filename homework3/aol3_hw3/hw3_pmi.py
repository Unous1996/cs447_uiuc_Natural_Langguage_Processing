########################################
## CS447 Natural Language Processing  ##
##           Homework 3               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Use pointwise mutual information to compare words in the movie corpora
##
import os.path
import sys
import numpy as np
import math
from operator import itemgetter
from collections import defaultdict

# ----------------------------------------
#  Data input 
# ----------------------------------------

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
# (taken from nested section of HW0)
def readFileToCorpus(f):
    """ Reads in the text file f which contains one sentence per line.
    """
    if os.path.isfile(f):
        file = open(f, "r")  # open the input file in read-only mode
        i = 0  # this is just a counter to keep track of the sentence numbers
        corpus = []  # this will become a list of sentences
        print("Reading file", f, "...")
        for line in file:
            i += 1
            sentence = line.split() # split the line into a list of words
            corpus.append(sentence) # append this list as an element to the list of sentences
            # if i % 1000 == 0:
            #    sys.stderr.write("Reading sentence " + str(i) + "\n") # just a status message: str(i) turns the integer i into a string, so that we can concatenate it
        return corpus
    else:
        print("Error: corpus file", f, "does not exist")  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
        sys.exit()  # exit the script

# --------------------------------------------------------------
# PMI data structure
# --------------------------------------------------------------
class PMI:
    # Given a corpus of sentences, store observations so that PMI can be calculated efficiently
    def __init__(self, corpus):
        self.corpus = corpus
        self.num_of_sentences = len(corpus)
        self.occurance = np.zeros(shape=(len(corpus),40000))
        self.word_to_index = {}
        self.column_sums = []
        self.__train()
        self.__trainColumnSum()
        print("\nYour task is to add the data structures and implement the methods necessary to efficiently get the pairwise PMI of words from a corpus")

    def __train(self):
        count = 0
        for i in range(len(self.corpus)):
            for word in self.corpus[i]:
                if word not in self.word_to_index.keys():
                    self.word_to_index[word] = count
                    count += 1
                    if count >= 40000:
                        self.occurance = np.c_[self.occurance,np.zeros(shape=(len(corpus),1))]
                word_index = self.word_to_index[word]
                self.occurance[i][word_index] = max(self.occurance[i][word_index], 1)

    def __trainColumnSum(self):
        for i in range(len(self.word_to_index)):
            self.column_sums.append(np.sum(self.occurance[:,i]))

    def __getLogProbSingle(self, word):
        word_index = self.word_to_index[word]
        #return math.log(np.sum(self.occurance[:,word_index]),2) - math.log(self.num_of_sentences,2)
        return math.log(self.column_sums[word_index], 2) - math.log(self.num_of_sentences, 2)

    def __getLogProbDouble(self, word1, word2):
        word_index1 = self.word_to_index[word1]
        word_index2 = self.word_to_index[word2]
        vector_1 = self.occurance[:,word_index1]
        vector_2 = self.occurance[:,word_index2]
        word_1_occurance = []
        word_2_occurance = []
        word_co_occurance = []
        for i in range(self.num_of_sentences):
            if vector_1[i] == 1:
                word_1_occurance.append(i)
            if vector_2[i] == 1:
                word_2_occurance.append(i)
            if vector_1[i]*vector_2[i] == 1:
                word_co_occurance.append(i)
        vector_3 = np.multiply(vector_1,vector_2)
        temp_log = math.log(np.sum(vector_3),2)
        return  temp_log - math.log(self.num_of_sentences,2)

    # Return the pointwise mutual information (based on sentence (co-)occurrence frequency) for w1 and w2
    def getPMI(self, w1, w2):
        word_pair = self.pair(w1=w1, w2=w2)
        log_prob1 = self.__getLogProbDouble(word1=word_pair[0], word2=word_pair[1])
        log_prob2 = self.__getLogProbSingle(word=word_pair[0])
        log_prob3 = self.__getLogProbSingle(word=word_pair[1])
        log_result = log_prob1 - log_prob2 - log_prob3
        return log_result

    # Given a frequency cutoff k, return the list of observed words that appear in at least k sentences
    def getVocabulary(self, k):
        print("\nSubtask 2: return the list of words where a word is in the list iff it occurs in at least k sentences")
        return ["the", "a", "to", "of", "in"]

    # Given a list of words and a number N, return a list of N pairs of words that have the highest PMI
    # (without repeated pairs, and without duplicate pairs (wi, wj) and (wj, wi)).
    # Each entry in the list should be a triple (pmiValue, w1, w2), where pmiValue is the
    # PMI of the pair of words (w1, w2)
    def getPairsWithMaximumPMI(self, words, N):
        print("\nSubtask 3: given a list of words and a number N, find N pairs of words with the greatest PMI")
        return [(1.0, "foo", "bar")]

    #-------------------------------------------
    # Provided PMI methods
    #-------------------------------------------
    # Writes the first numPairs entries in the list of wordPairs to a file, along with each pair's PMI
    def writePairsToFile(self, numPairs, wordPairs, filename): 
        f=open(filename, 'w+')
        count = 0
        for (pmiValue, wi, wj) in wordPairs:
            if count > numPairs:
                break
            count += 1
            print("%f %s %s" % (pmiValue, wi, wj), end="\n", file=f)

    # Helper method: given two words w1 and w2, returns the pair of words in sorted order
    # That is: pair(w1, w2) == pair(w2, w1)
    def pair(self, w1, w2):
        return (min(w1, w2), max(w1, w2))

#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    corpus = readFileToCorpus('movies.txt')
    pmi = PMI(corpus)
    lv_pmi = pmi.getPMI("luke", "vader")
    print("  PMI of \"luke\" and \"vader\": ", lv_pmi)
    numPairs = 100
    k = 200
    # for k in 2, 5, 10, 50, 100, 200:
    commonWords = pmi.getVocabulary(k)    # words must appear in least k sentences
    wordPairsWithGreatestPMI = pmi.getPairsWithMaximumPMI(commonWords, numPairs)
    pmi.writePairsToFile(wordPairsWithGreatestPMI, "pairs_minFreq="+str(k)+".txt")

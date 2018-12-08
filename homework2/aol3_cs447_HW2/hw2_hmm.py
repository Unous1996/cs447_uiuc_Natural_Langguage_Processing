########################################
## CS447 Natural Language Processing  ##
##           Homework 2               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Train a bigram HMM for POS tagging
##
import os.path
import sys
from operator import itemgetter
from collections import defaultdict
from math import log, exp
import copy

# Unknown word token
UNK = 'UNK'

# Class that stores a word and tag together
class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_');
        self.word = parts[0]
        self.tag = parts[1]

# Class definition for a bigram HMM
class HMM:
### Helper file I/O methods ###
    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads a labeled data inputFile, and returns a nested list of sentences, where each sentence is a list of TaggedWord objects
    def readLabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = [];
            for line in file:
                raw = line.split()
                sentence = []
                for token in raw:
                    sentence.append(TaggedWord(token))
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s does not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script

    ################################
    #intput:                       #
    #    inputFile: string         #
    #output: list                  #
    ################################
    # Reads an unlabeled data inputFile, and returns a nested list of sentences, where each sentence is a list of strings
    def readUnlabeledData(self, inputFile):
        if os.path.isfile(inputFile):
            file = open(inputFile, "r") # open the input file in read-only mode
            sens = [];
            for line in file:
                sentence = line.split() # split the line into a list of words
                sens.append(sentence) # append this list as an element to the list of sentences
            return sens
        else:
            print("Error: unlabeled data file %s ddoes not exist" % inputFile)  # We should really be throwing an exception here, but for simplicity's sake, this will suffice.
            sys.exit() # exit the script
### End file I/O methods ###

    ################################
    #intput:                       #
    #    unknownWordThreshold: int #
    #output: None                  #
    ################################
    # Constructor
    def __init__(self, unknownWordThreshold=5):
        # Unknown word threshold, default value is 5 (words occuring fewer than 5 times should be treated as UNK)
        self.minFreq = unknownWordThreshold
        self.single_hidden = {}
        self.double_hidden = {}
        self.begin_hidden = {}
        self.single_word = {}
        self.emission = {}
        #self.tag_following_word = {}
        self.tag_following_tag = {}
        self.tags = set()
        self.tags_list = []
        self.num_of_sentences = 0.0
        ### Initialize the rest of your data structures here ###

    ################################
    #intput:                       #
    #    trainFile: string         #
    #output: None                  #
    ################################
    # Given labeled corpus in trainFile, build the HMM distributions from the observed counts
    def train(self, trainFile):
        data = self.readLabeledData(trainFile)  # data is a nested list of TaggedWords
        self.num_of_sentences = len(data)
        #Phase 1:
        for sen in data:
            for tagged_word in sen:
                if not (tagged_word.word in self.single_word):
                    self.single_word[tagged_word.word] = 1
                else:
                    self.single_word[tagged_word.word] += 1

        #Phase 2:
        for sen in data:
            prev_tagged_word = sen[0]
            #check whether prev_tagged_word is not a rare word
            #If it is, replace its word portion with UNK
            if self.single_word[prev_tagged_word.word] < self.minFreq:
                prev_tagged_word.word = UNK

            if not (prev_tagged_word.tag in self.single_hidden):
                self.single_hidden[prev_tagged_word.tag] = 1.0
            else:
                self.single_hidden[prev_tagged_word.tag] += 1.0

            if not ((prev_tagged_word.word, prev_tagged_word.tag) in self.emission):
                self.emission[(prev_tagged_word.word, prev_tagged_word.tag)] = 1.0
            else:
                self.emission[(prev_tagged_word.word, prev_tagged_word.tag)] += 1.0

            self.tags.add(prev_tagged_word.tag)

            if prev_tagged_word.tag not in self.begin_hidden:
                self.begin_hidden[prev_tagged_word.tag] = 1.0
            else:
                self.begin_hidden[prev_tagged_word.tag] += 1.0

            for tagged_word in sen[1:]:
                #check whether tagged_word is not a rare word
                #If it is, replace its word portion with UNK
                if self.single_word[tagged_word.word] < self.minFreq:
                    tagged_word.word = UNK

                if not(tagged_word.tag in self.single_hidden):
                    self.single_hidden[tagged_word.tag] = 1.0
                else:
                    self.single_hidden[tagged_word.tag] += 1.0

                if not((prev_tagged_word.tag, tagged_word.tag) in self.double_hidden):
                    self.double_hidden[(prev_tagged_word.tag, tagged_word.tag)] = 1.0
                else:
                    self.double_hidden[(prev_tagged_word.tag, tagged_word.tag)] += 1.0

                if not((tagged_word.word, tagged_word.tag) in self.emission):
                    self.emission[(tagged_word.word, tagged_word.tag)] = 1.0
                else:
                    self.emission[(tagged_word.word, tagged_word.tag)] += 1.0

                self.tags.add(tagged_word.tag)

                if not prev_tagged_word.tag in self.tag_following_tag:
                    self.tag_following_tag[prev_tagged_word.tag] = set([tagged_word.tag])
                else:
                    self.tag_following_tag[prev_tagged_word.tag].add(tagged_word.tag)

                prev_tagged_word = tagged_word

        self.tags_list = list(self.tags)
        #print("Your first task is to train a bigram HMM tagger from an input file of POS-tagged text")

    ################################
    #intput:                       #
    #     testFile: string         #
    #    outFile: string           #
    #output: None                  #
    ################################
    # Given an unlabeled corpus in testFile, output the Viterbi tag sequences as a labeled corpus in outFile
    def test(self, testFile, outFile):
        data = self.readUnlabeledData(testFile)
        f=open(outFile, 'w+')
        for sen in data:
            vitTags = self.viterbi(sen)
            senString = ''
            for i in range(len(sen)):
                senString += sen[i]+"_"+vitTags[i]+" "
            print(senString)
            print(senString.rstrip(), end="\n", file=f)


    def __getObservedProb(self, word, tag):
        if (word, tag) in self.emission:
            numerator = self.emission[(word, tag)]
        else:
            numerator = 0
        denominator = self.single_hidden[tag]
        return numerator/denominator


    def __getLogObservedProb(self, word, tag):
        pass
        if (word, tag) in self.emission:
            numerator = self.emission[(word, tag)]
        else:
            return 1.0
        denominator = self.single_hidden[tag]
        return log(numerator) - log(denominator)


    def __getStartObservedProb(self, tag):
        if tag in self.begin_hidden:
            return self.begin_hidden[tag]/self.num_of_sentences
        else:
            return 0


    def __getLogStartObservedProb(self, tag):
        if tag in self.begin_hidden:
            return log(self.begin_hidden[tag]) - log(self.num_of_sentences)
        else:
            return 1.0

    def __getTransitionProb(self, currtag, prevtag):
        K = 1
        if (prevtag,currtag) not in self.double_hidden:
            numerator = 1
        else:
            numerator = self.double_hidden[(prevtag, currtag)] + K

        denominator = self.single_hidden[prevtag]+K*len(self.tag_following_tag[prevtag])
        return numerator/denominator


    def __getLogTransitionProb(self, currtag, prevtag):
        if (prevtag,currtag) not in self.double_hidden:
            numerator = 1
        else:
            numerator = self.double_hidden[(prevtag, currtag)] + 1

        denominator = self.single_hidden[prevtag]+len(self.tag_following_tag[prevtag])
        return log(numerator) - log(denominator)


    def __helperfun(self, input):
        if input == 1.0:
            return 0
        else:
            return -1/input
    ################################
    #intput:                       #
    #    words: list               #
    #output: list                  #
    ################################
    # Given a list of words, runs the Viterbi algorithm and returns a list containing the sequence of tags
    # that generates the word sequence with highest probability, according to this HMM
    def viterbi(self, words):

        trellis = [[1.0 for x in range(len(self.tags_list))] for y in range(2)]
        backpointer = [[-1 for x in range(len(words))] for y in range(len(self.tags_list))]
        return_list = []

        for tag in self.tags_list:
            temp_prob = self.__getLogStartObservedProb(tag)
            trellis[0][self.tags_list.index(tag)] = temp_prob

        for i in range(len(words)):
            for j in range(len(self.tags_list)):
                log_max_prob = 1.0
                if not words[i] in self.single_word or self.single_word[words[i]] < self.minFreq:
                    log_temp_prob = self.__getLogObservedProb(word = UNK, tag = self.tags_list[j])
                    if log_temp_prob != 1.0:
                        trellis[1][j] = log_temp_prob
                    else:
                        continue
                else:
                    log_temp_prob = self.__getLogObservedProb(word = words[i], tag = self.tags_list[j])
                    if log_temp_prob != 1.0:
                        trellis[1][j] = log_temp_prob
                    else:
                        continue

                for k in range(len(self.tags_list)):
                    log_temp_prob = self.__getLogTransitionProb(currtag=self.tags_list[j], prevtag=self.tags_list[k])
                    if trellis[0][k] != 1.0 and log_temp_prob != 1.0:
                        if log_max_prob == 1.0:
                            log_max_prob = trellis[0][k] + log_temp_prob
                            #max_index_list[j] = k
                            backpointer[j][i] = k
                        else:
                            if log_temp_prob + trellis[0][k] > log_max_prob:
                                log_max_prob = trellis[0][k] + log_temp_prob
                                #max_index_list[j] = k
                                backpointer[j][i] = k

                trellis[1][j] += log_max_prob

            #max_index = trellis[1].index(max(trellis[1], key=self.__helperfun))
            #return_list.append(self.tags_list[max_index])
            max_index_list = [-1 for x in range((len(self.tags_list)))]
            trellis[0] = copy.deepcopy(trellis[1])
            trellis[1] = [1.0 for i in range(len(self.tags_list))]

        #backpropagation phase

        prev_max_index = trellis[0].index(max(trellis[0], key=self.__helperfun))
        return_list.append(self.tags_list[prev_max_index])
        for i in range(len(words)-1,0,-1):
            return_list.insert(0, self.tags_list[backpointer[prev_max_index][i]])
            prev_max_index = backpointer[prev_max_index][i]

        return return_list# this returns a dummy list of "NULL", equal in length to words

if __name__ == "__main__":
    tagger = HMM()
    tagger.train('train.txt')
    tagger.test('test.txt', 'out.txt')

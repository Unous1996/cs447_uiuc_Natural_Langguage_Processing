########################################
## CS447 Natural Language Processing  ##
##           Homework 2               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Evaluate the output of your bigram HMM POS tagger
##
import os.path
import sys
import numpy as np
from operator import itemgetter

class TaggedWord:
    def __init__(self, taggedString):
        parts = taggedString.split('_');
        self.word = parts[0]
        self.tag = parts[1]

# A class for evaluating POS-tagged data
class Eval:

    ################################
    #intput:                       #
    #    goldFile: string          #
    #    testFile: string          #
    #output: None                  #
    ################################
    def __init__(self, goldFile, testFile):
        self.gold_data = self.readLabeledData(goldFile)
        self.test_data = self.readLabeledData(testFile)
        self.tag_set = set()
        self.__getSentenceAccuracyAndSetOfTags()
        self.tag_list = list(self.tag_set)
        self.confusion_matrix = np.zeros((len(self.tag_list),len(self.tag_list)))
        self.token_accuracy = 0.0
        self.__getConfusionMatrixAndTheTokenAccuracy()
        print("Your task is to implement an evaluation program for POS tagging")

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
    #intput: None                  #
    #output: float                 #
    ################################
    def getTokenAccuracy(self):
        '''
        correct = 0.0
        incorrect = 0.0
        if len(self.gold_data) != len(self.test_data):
            print("Warning: the numbers of the sentences in the test file and golden file are different")
        for i in range(len(self.gold_data)):
            if len(self.gold_data[i]) != len(self.test_data[i]):
                print("Warning: the number of words in the",i,"th sentence in the test data differs from that of gold data")
            for j in range(len(self.gold_data[i])):
                if self.gold_data[i][j].tag != self.test_data[i][j].tag:
                    incorrect += 1.0
                else:
                    correct += 1.0
        return correct/(correct + incorrect)
        '''
        return self.token_accuracy

    ################################
    #intput: None                  #
    #output: float                 #
    ################################

    def __getSentenceAccuracyAndSetOfTags(self):
        correct = 0.0
        incorrect = 0.0
        for i in range(len(self.gold_data)):
            correct_tag = True
            for j in range(len(self.gold_data[i])):
                self.tag_set.add(self.gold_data[i][j].tag)
                if self.gold_data[i][j].tag != self.test_data[i][j].tag:
                    correct_tag = False
                    self.tag_set.add(self.test_data[i][j].tag)

            if correct_tag:
                correct += 1.0

        self.sentence_accuracy = correct/len(self.gold_data)

    def __getConfusionMatrixAndTheTokenAccuracy(self):
        correct = 0.0
        incorrect = 0.0
        for i in range(len(self.gold_data)):
            for j in range(len(self.gold_data[i])):
                golden_index = self.tag_list.index(self.gold_data[i][j].tag)
                test_index = self.tag_list.index(self.test_data[i][j].tag)
                self.confusion_matrix[golden_index][test_index] += 1.0
                if golden_index == test_index:
                    correct += 1.0
                else:
                    incorrect += 1.0

        self.token_accuracy = correct/(correct + incorrect)


    def getSentenceAccuracy(self):
        return self.sentence_accuracy

    ################################
    #intput:                       #
    #    outFile: string           #
    #output: None                  #
    ################################
    def writeConfusionMatrix(self, outFile):
        np.savetxt(outFile, self.confusion_matrix)

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    def getPrecision(self, tagTi):
        tag_index = self.tag_list.index(tagTi)
        return self.confusion_matrix[tag_index][tag_index]/np.sum(self.confusion_matrix[:,tag_index])

    ################################
    #intput:                       #
    #    tagTi: string             #
    #output: float                 #
    ################################
    # Return the tagger's recall on gold tag t_j
    def getRecall(self, tagTj):
        #print("Return the tagger's recall for correctly predicting gold tag t_j")
        tag_index = self.tag_list.index(tagTj)
        return self.confusion_matrix[tag_index][tag_index]/np.sum(self.confusion_matrix[tag_index])


if __name__ == "__main__":
    # Pass in the gold and test POS-tagged data as arguments
    if len(sys.argv) < 2:
        print("Please Call hw2_eval_hmm.py with two arguments: gold.txt and out.txt")
    else:
        gold = sys.argv[1]
        test = sys.argv[2]
        # You need to implement the evaluation class
        eval = Eval(gold, test)
        # Calculate accuracy (sentence and token level)
        print("Token accuracy: ", eval.getTokenAccuracy())
        print("Sentence accuracy: ", eval.getSentenceAccuracy())
        # Calculate recall and precision
        print("Recall on tag NNP: ", eval.getRecall('NNP'))
        print("Precision for tag NNP: ", eval.getPrecision('NNP'))
        # Write a confusion matrix
        eval.writeConfusionMatrix("conf_matrix.txt")

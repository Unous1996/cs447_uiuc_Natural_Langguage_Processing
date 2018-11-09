import sys
import os
import math

# The start symbol for the grammar
TOP = "TOP"

'''
A grammatical Rule has a probability and a parent category, and is
extended by UnaryRule and BinaryRule
'''

class Rule:

    def __init__(self, probability, parent):
        self.prob = probability
        self.parent = parent

    # Factory method for making unary or binary rules (returns None otherwise)
    @staticmethod
    def createRule(probability, parent, childList):
        if len(childList) == 1:
            return UnaryRule(probability, parent, childList[0])
        elif len(childList) == 2:
            return BinaryRule(probability, parent, childList[0], childList[1])
        return None

    # Returns a tuple containing the rule's children
    def children(self):
        return ()

'''
A UnaryRule has a probability, a parent category, and a child category/word
'''

class UnaryRule(Rule):

    def __init__(self, probability, parent, child):
        Rule.__init__(self, probability, parent)
        self.child = child

    # Returns a singleton (tuple) containing the rule's child
    def children(self):
        return (self.child,)  # note the comma; (self.child) is not a tuple

'''
A BinaryRule has a probability, a parent category, and two children
'''


class BinaryRule(Rule):

    def __init__(self, probability, parent, leftChild, rightChild):
        Rule.__init__(self, probability, parent)
        self.leftChild = leftChild
        self.rightChild = rightChild

    # Returns a pair (tuple) containing the rule's children
    def children(self):
        return (self.leftChild, self.rightChild)

'''
An Item stores the label and Viterbi probability for a node in a parse tree
'''

class Item:
    def __init__(self, label, prob, numParses):
        self.label = label #key
        self.prob = prob
        self.numParses = numParses

    # Returns the node's label
    def toString(self):
        return self.label

'''
A LeafItem is an Item that represents a leaf (word) in the parse tree (ie, it
doesn't have children, and it has a Viterbi probability of 1.0)
'''

class LeafItem(Item):

    def __init__(self, word):
        # using log probabilities, this is the default value (0.0 = log(1.0))
        self.numParses = 1
        Item.__init__(self, word, 0.0, 1)

'''
An InternalNode stores an internal node in a parse tree (ie, it also
stores pointers to the node's child[ren])
'''


class InternalItem(Item):

    def __init__(self, category, prob, children=()):
        Item.__init__(self, category, prob, 0)
        self.children = children
        # Your task is to update the number of parses for this InternalItem
        # to reflect how many possible parses are rooted at this label
        # for the string spanned by this item in a chart
        self.numParses = 1 # dummy numParses value; this should not be -1!
        for child in self.children:
            self.numParses *= child.numParses

        if len(self.children) > 2:
            print("Warning: adding a node with more than two children (CKY may not work correctly)")
            #is it the maximum child? / the best backtracking pointer

    # For an internal node, we want to recurse through the labels of the
    # subtree rooted at this node
    def toString(self):
        ret = "( " + self.label + " "
        for child in self.children:
            ret += child.toString() + " "
        return ret + ")"

'''
A Cell stores all of the parse tree nodes that share a common span

Your task is to implement the stubs provided in this class
'''

class Cell:

    def __init__(self):
        self.dict_items = {}

    def addItem(self, item):
        # Add an Item to this cell
        # If the parent(label) is different, we just add the item,
        # however, if the parent is the same, we need to
        # a. compare the probability
        # b. modify the backward pointer(children)
        if item.label not in self.dict_items.keys():
            self.dict_items[item.label] = item
        else:
            original_item = self.dict_items[item.label]
            original_parses = original_item.numParses
            newcoming_parses = item.numParses
            if item.prob > original_item.prob:
                self.dict_items[item.label] = item
                item.numParses = original_parses + newcoming_parses
            else:
                original_item.numParses = original_parses + newcoming_parses

    def addLeafItem(self, item):
        self.dict_items[item.label] = item

    def getItem(self, label):
        return self.dict_items[label]

    def getItems(self):
        return self.dict_items.values()

'''
A Chart stores a Cell for every possible (contiguous) span of a sentence

Your task is to implement the stubs provided in this class
'''


class Chart:

    def __init__(self, sentence):
        # Initialize the chart, given a sentence
        self.words =sentence
        self.cells = [[ Cell() for j in range(len(self.words))] for i in range(len(self.words)+1)]
        self.supercell = Cell()

    def getRoot(self):
        #return the maximum probability item
        critical_cell = self.supercell
        mark = False
        max_item = None
        for key in critical_cell.dict_items.keys():
            if key == 'TOP':
                if not mark:
                    mark = True
                    max_item = critical_cell.dict_items[key]
                else:
                    if critical_cell.dict_items[key].prob > max_item.prob:
                        max_item = critical_cell.dict_items[key]
        return max_item

    def getCell(self, i, j):
        critical_cell = self.cells[i][j]
        mark = False
        max_item = None
        for key in critical_cell.dict_items.keys():
            if critical_cell.dict_items[key] == TOP:
                if not mark:
                    mark = True
                    max_item = critical_cell.dict_items[key]
                else:
                    if critical_cell.dict_items[key].prob > max_item.prob:
                        max_item = critical_cell.dict_items[key]
        return max_item

'''
A PCFG stores grammatical rules (with probabilities), and can be used to
produce a Viterbi parse for a sentence if one exists
'''

class PCFG:

    def __init__(self, grammarFile, debug=False):
        # in ckyRules, keys are the rule's RHS (the rule's children, stored in
        # a tuple), and values are the parent categories
        self.ckyRules = {}
        self.debug = debug                  # boolean flag for debugging
        # reads the probabilistic rules for this grammar
        self.readGrammar(grammarFile)
        # checks that the grammar at least matches the start symbol defined at
        # the beginning of this file (TOP)
        self.topCheck()

    '''
    Reads the rules for this grammar from an input file
    '''

    def readGrammar(self, grammarFile):
        if os.path.isfile(grammarFile):
            file = open(grammarFile, "r")
            for line in file:
                raw = line.split()
                # reminder, we're using log probabilities
                prob = math.log(float(raw[0]))
                parent = raw[1]
                children = raw[
                    3:]   # Note: here, children is a list; below, rule.children() is a tuple
                rule = Rule.createRule(prob, parent, children)
                if rule.children() not in self.ckyRules:
                    self.ckyRules[rule.children()] = set([])
                self.ckyRules[rule.children()].add(rule)

    '''
    Checks that the grammar at least matches the start symbol (TOP)
    '''

    def topCheck(self):
        for rhs in self.ckyRules:
            for rule in self.ckyRules[rhs]:
                if rule.parent == TOP:
                    return  # TOP generates at least one other symbol
        if self.debug:
            print("Warning: TOP symbol does not generate any children (grammar will always fail)")

    '''
    Your task is to implement this method according to the specification. You may define helper methods as needed.

    Input:        sentence, a list of word strings
    Returns:      The root of the Viterbi parse tree, i.e. an InternalItem with label "TOP" whose probability is the Viterbi probability.
                   By recursing on the children of this node, we should be able to get the complete Viterbi tree.
                   If no such tree exists, return None\
    '''

    def CKY(self, sentence):
        # dummy return value:
        CKY_chart = Chart(sentence)
        for j in range(0,len(sentence)):
            for rule in self.ckyRules[(sentence[j],)]:
                CKY_chart.cells[j+1][j].addLeafItem(LeafItem(word=rule.child))
                child_tuple = (CKY_chart.cells[j+1][j].dict_items[rule.child],)
                CKY_chart.cells[j][j].addItem(InternalItem(category=rule.parent, prob=rule.prob,children=child_tuple))
            for i in range(j-1,-1,-1):
                for k in range(i, j):
                    for rhs in self.ckyRules:
                        for rule in self.ckyRules[rhs]:
                            if len(rhs) == 2:
                                if rule.leftChild in CKY_chart.cells[i][k].dict_items.keys() and rule.rightChild in CKY_chart.cells[k+1][j].dict_items.keys():
                                    left_prob = CKY_chart.cells[i][k].dict_items[rule.leftChild].prob
                                    right_prob = CKY_chart.cells[k+1][j].dict_items[rule.rightChild].prob
                                    child_tuple = (CKY_chart.cells[i][k].dict_items[rule.leftChild], CKY_chart.cells[k+1][j].dict_items[rule.rightChild])
                                    CKY_chart.cells[i][j].addItem(InternalItem(category=rule.parent, prob=rule.prob + left_prob + right_prob, children=child_tuple))

        for rhs in self.ckyRules:
            for rule in self.ckyRules[rhs]:
                if rule.parent == 'TOP' and len(rhs) == 1:
                    if rule.child in CKY_chart.cells[0][len(sentence)-1].dict_items.keys():
                        child_prob = CKY_chart.cells[0][len(sentence)-1].dict_items[rule.child].prob
                        child_tuple = (CKY_chart.cells[0][len(sentence)-1].dict_items[rule.child],)
                        CKY_chart.supercell.addItem(InternalItem(category=rule.parent, prob=child_prob + rule.prob, children=child_tuple))


        return CKY_chart.getRoot()


if __name__ == "__main__":
    pcfg = PCFG('toygrammar.pcfg')
    sen = "the man eats the sushi".split()
    tree = pcfg.CKY(sen)

    if tree is not None:
        print(tree.toString())
        print("Probability: " + str(math.exp(tree.prob)))
        print("Num parses: " + str(tree.numParses))
    else:
        print("Parse failure!")

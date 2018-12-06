# Constant for NULL word at position zero in target sentence
NULL = "NULL"
import math

# Your task is to finish implementing IBM Model 1 in this class
class IBMModel1:

    def __init__(self, trainingCorpusFile):
        # Initialize data structures for storing training data
        self.fCorpus = []                   # fCorpus is a list of foreign (e.g. Spanish) sentences
        self.tCorpus = []                   # tCorpus is a list of target (e.g. English) sentences
        self.length_dict = {}
        self.trans = {}                     # trans[e_i][f_j] is initialized with a count of how often target word e_i and foreign word f_j appeared together.
        self.prob_trans = {}                # self.prob_trans[][]
        self.trans_new = {}
        self.z = {}
        self.c = {}
        # Read the corpus
        self.initialize(trainingCorpusFile);
        # Initialize any additional data structures here (e.g. for probability model)

    # Reads a corpus of parallel sentences from a text file (you shouldn't need to modify this method)
    def initialize(self, fileName):
        f = open(fileName)
        i = 0
        j = 0;
        tTokenized = ();
        fTokenized = ();
        for s in f:
            if i == 0:
                tTokenized = s.split()
                # Add null word in position zero
                tTokenized.insert(0, NULL)
                self.tCorpus.append(tTokenized)
            elif i == 1:
                fTokenized = s.split()
                self.fCorpus.append(fTokenized)
                for tw in tTokenized:
                    if tw not in self.trans:
                        self.trans[tw] = {};
                    for fw in fTokenized:
                        if fw not in self.trans[tw]:
                             self.trans[tw][fw] = 1
                        else:
                            self.trans[tw][fw] =  self.trans[tw][fw] +1
            else:
                i = -1
                j += 1
            i +=1
        f.close()
        return

    # Uses the EM algorithm to learn the model's parameters
    def trainUsingEM(self, numIterations=10, writeModel=False, convergenceEpsilon=0.01):
        ###
        # Part 1: Train the model using the EM algorithm
        #
        # <you need to finish implementing this method's sub-methods>
        #
        ###
        # Compute translation length probabilities q(m|n)
        self.computeTranslationLengthProbabilities()         # <you need to implement computeTranslationlengthProbabilities()>
        # Set initial values for the translation probabilities p(f|e)
        self.initializeWordTranslationProbabilities()        # <you need to implement initializeTranslationProbabilities()>
        # Write the initial distributions to file

        if writeModel:
            self.printModel('initial_model.txt')                 # <you need to implement printModel(filename)>
        for i in range(numIterations):
            print("Starting training iteration "+str(i))
            # Run E-step: calculate expected counts using current set of parameters
            self.computeExpectedCounts()                     # <you need to implement computeExpectedCounts()>
            print("finished computing expected counts")
            # Run M-step: use the expected counts to re-estimate the parameters
            self.updateTranslationProbabilities()            # <you need to implement updateTranslationProbabilities()>
            print("update translation probabilites")
            # Write model distributions after iteration i to file
            if writeModel:
                self.printModel('model_iter='+str(i)+'.txt')     # <you need to implement printModel(filename)>

    # Compute translation length probabilities q(m|n)
    def computeTranslationLengthProbabilities(self):
        # Implement this method
        for i in range(len(self.tCorpus)):
            f_length = len(self.fCorpus[i])
            t_length = len(self.tCorpus[i])
            if t_length in self.length_dict.keys():
                self.length_dict[t_length].add(f_length)
            else:
                self.length_dict[t_length] = {f_length}

    # Set initial values for the translation probabilities p(f|e)
    def initializeWordTranslationProbabilities(self):
        # Implement this method
        for e_word in self.trans.keys():

            if e_word not in self.prob_trans.keys():
                self.prob_trans[e_word] = {}
            f_sum = 0

            for f_word in self.trans[e_word].keys():

                if f_word not in self.prob_trans[e_word].keys():
                    self.prob_trans[e_word][f_word] = 1
                f_sum += 1
                self.prob_trans[e_word][f_word] = math.log(self.trans[e_word][f_word]) - math.log(f_sum)

    # Run E-step: calculate expected counts using current set of parameters
    def computeExpectedCounts(self):
        # Implement this method（E Phase）
        self.c = {}

        for s_index in range(len(self.tCorpus)):
            for e_i in self.tCorpus[s_index]:
                if e_i not in self.c.keys():
                    self.c[e_i] = {}

                for f_j in self.fCorpus[s_index]:
                    if f_j not in self.c[e_i].keys():
                        self.c[e_i][f_j] = 0

                    nominator = math.exp(self.prob_trans[e_i][f_j])
                    dominator = 0

                    for e in self.tCorpus[s_index]:
                        if f_j in self.prob_trans[e].keys() and self.prob_trans[e][f_j] != 1:
                            dominator += math.exp(self.prob_trans[e][f_j])

                    self.c[e_i][f_j] += nominator/dominator

    # Run M-step: use the expected counts to re-estimate the parameters
    def updateTranslationProbabilities(self):
        # Implement this method(Normalization Phase)
        z = {}
        for e_x in self.c.keys():
            if e_x not in z.keys():
                z[e_x] = 0
            for f_y in self.c[e_x].keys():
                z[e_x] += self.c[e_x][f_y]

        self.prob_trans = {}
        for e in self.c.keys():
            if e not in self.prob_trans.keys():
                self.prob_trans[e] = {}
            for f in self.c[e].keys():
                if f not in self.prob_trans[e].keys():
                    self.prob_trans[e][f] = 1
                self.prob_trans[e][f] = math.log(self.c[e][f]) - math.log(z[e])

    # Returns the best alignment between fSen and tSen, according to your model
    def align(self, fSen, tSen):
        ###
        # Part 2: Find and return the best alignment
        # <you need to finish implementing this method>
        # Remove the following code (a placeholder return that aligns each foreign word with the null word in position zero of the target sentence)
        ###

        returnAlignment = []
        for f_word in fSen:
            max_t_word_index = 0
            max_prob = self.getWordTranslationProbability(f_j=f_word, e_i=tSen[0])
            for i in range(len(tSen)): #here we assume that "tSen" begin with "NULL"
                new_prob = self.getWordTranslationProbability(f_j=f_word, e_i=tSen[i])
                if new_prob > max_prob:
                    max_prob = new_prob
                    max_t_word_index = i
            returnAlignment.append(max_t_word_index)

        return returnAlignment   # Your code above should return the correct alignment inst

    # Return q(fLength | tLength), the probability of producing an English sentence of length tLength given a non-English sentence of length fLength
    # (Can either return log probability or regular probability)
    def getTranslationLengthProbability(self, fLength, tLength):
        # Implement this method
        if fLength in self.length_dict[tLength]:
            return -math.log(len(self.length_dict[tLength]))
        else:
            return -float('inf')

    # Return p(f_j | e_i), the probability that English word e_i generates non-English word f_j
    # (Can either return log probability or regular probability)
    def getWordTranslationProbability(self, f_j, e_i):
        # Implement this method
        if e_i in self.prob_trans.keys():
            if f_j in self.prob_trans[e_i].keys():
                if self.prob_trans[e_i][f_j] == 1:
                    return -float('inf')
                else:
                    return self.prob_trans[e_i][f_j]
        return -float('inf')

    # Write this model's probability distributions to file
    def printModel(self, filename):
        lengthFile = open(filename+'_lengthprobs.txt', 'w')         # Write q(m|n) for all m,n to this file
        translateProbFile = open(filename+'_translationprobs.txt', 'w') # Write p(f_j | e_i) for all f_j, e_i to this file
        # Implement this method (make your output legible and informative)
        # length_chart = self.length_dict
        # Modifying length_dict

        for n in self.length_dict:
            string = ""
            for m in self.length_dict.keys():
                temp_prob = math.exp(self.getTranslationLengthProbability(fLength=m, tLength=n))
                if temp_prob > 0:
                    string += "Pr (m = {0} | n = {1}) = {2} ".format(m, n, round(temp_prob,2))
            lengthFile.write(string)
            lengthFile.write('\n')
            lengthFile.write('\n')

        for e_i in self.prob_trans.keys():
            string = ""
            for f_j in self.prob_trans[e_i].keys():
                temp_prob = round(math.exp(self.getWordTranslationProbability(f_j=f_j, e_i=e_i)), 2)
                if temp_prob > 0.005:
                    string += "Pr (f_y = {0} | e_x = {1}) = {2} ".format(f_j, e_i, temp_prob)
            translateProbFile.write(string)
            translateProbFile.write('\n')
            translateProbFile.write('****************************************************************')
            translateProbFile.write('\n')

        lengthFile.close()
        translateProbFile.close()

# utility method to pretty-print an alignment
# You don't have to modify this function unless you don't think it's that pretty...
def prettyAlignment(fSen, tSen, alignment):
    pretty = ''
    for j in range(len(fSen)):
        pretty += str(j)+'  '+fSen[j].ljust(20)+'==>    '+tSen[alignment[j]]+'\n';
    return pretty

if __name__ == "__main__":
    # Initialize model
    model = IBMModel1('eng-spa.txt')
    # Train model
    model.trainUsingEM(1);
    model.printModel('after_training')
    # Use model to get an alignment
    fSen = 'No pierdas el tiempo por el camino .'.split()
    tSen = 'Don\' t dawdle on the way'.split()
    alignment = model.align(fSen, tSen);
    print (prettyAlignment(fSen, tSen, alignment))

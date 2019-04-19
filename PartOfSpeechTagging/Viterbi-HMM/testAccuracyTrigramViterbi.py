# -*- coding: utf-8 -*-

from __future__ import division
import codecs, time
from collections import defaultdict
from trigramViterbi import trigramHMMViterbiAlgorithm, calculateTransitionProbabilities, calculateEmissionProbabilities


def main():
    Lambdas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    for Lambda in Lambdas:

        # Opening the input training file
        trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")

        # Getting the emission probabilities
        emissionProbabilityDict = calculateEmissionProbabilities(trainFile, Lambda)

        # Opening the input training file
        trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")

        # Getting the transition probabilities and all the tags (states)
        transitionProbabilityDict, allTags = calculateTransitionProbabilities(trainFile, Lambda)

        # Opening the input test file
        testFile = codecs.open("testDataHindi.txt", mode = "r", encoding = "utf-8")
        # Calling the test function to get the accuracy of algorithm on the test data file
        accuracy = testTrigramHMMViterbiAlgorithm(testFile, allTags, emissionProbabilityDict, transitionProbabilityDict)
        print(accuracy)
        time.sleep(5)

def testTrigramHMMViterbiAlgorithm(testFile, allTags, emissionProbabilityDict, transitionProbabilityDict):

    total = 0
    correct = 0
    for line in testFile.readlines():

        tokens = line.split()

        sentence = []

        tags = []

        for token in tokens:

            word = token.split('|')[0].strip()

            tag = token.split('|')[2].split('.')[0].strip(':?').strip()
            if (tag == 'I-NP' or tag == 'B-NP' or tag == 'O'):
                tag = 'NN'

            sentence.append(word)

            tags.append(tag)

        if sentence != []:
            actual = zip(sentence, tags)


            try:
                predicted = trigramHMMViterbiAlgorithm(sentence, allTags, emissionProbabilityDict, transitionProbabilityDict)
                for i in range(len(sentence)):
                    actualTag = actual[i][1]
                    predictedTag = predicted[i][1]

                    if actual[i][1] == predicted[i][1]:
                        correct += 1
                    print "CORRECT : " + str(correct) ,
                    total += 1
                    print " TOTAL   : " + str(total)
                    if total % 1000 == 0:
                        print(correct/total)
                        time.sleep(1)
            except:
                print("Couldn't Tag Sentence")
                continue

    return correct/total

if __name__ == "__main__":
    main()

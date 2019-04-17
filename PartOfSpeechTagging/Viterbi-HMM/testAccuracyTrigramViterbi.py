# -*- coding: utf-8 -*-

from __future__ import division
import codecs
from collections import defaultdict
from trigramViterbi import trigramHMMViterbiAlgorithm, calculateTransitionProbabilities, calculateEmissionProbabilities


def main():

    # Opening the input training file
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")
    # Getting the emission probabilities
    emissionProbabilityDict = calculateEmissionProbabilities(trainFile)
    # Opening the input training file
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")
    # Getting the transition probabilities and all the tags (states)
    transitionProbabilityDict, allTags = calculateTransitionProbabilities(trainFile)

    # Opening the input test file
    testFile = codecs.open("testDataHindi.txt", mode = "r", encoding = "utf-8")
    # Calling the test function to get the accuracy of algorithm on the test data file
    testTrigramHMMViterbiAlgorithm(testFile, allTags, emissionProbabilityDict, transitionProbabilityDict)


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

        # tags = tags[:-1]
        # sentence = sentence.strip().strip(".").strip()

        if sentence != []:
            actual = zip(sentence, tags)
            # print("\n\nACTUAL:\n\n")
            # print(actual)
            try:
                predicted = trigramHMMViterbiAlgorithm(sentence, allTags, emissionProbabilityDict, transitionProbabilityDict)
                for i in range(len(sentence)):
                    actualTag = actual[i][1]
                    predictedTag = predicted[i][1]
                    # print(actualTag, predictedTag)
                    if actual[i][1] == predicted[i][1]:
                        correct += 1
                    print "CORRECT : " + str(correct) ,
                    total += 1
                    print " TOTAL   : " + str(total)
            except:
                print("Couldn't Tag Sentence")
                continue
            # print("\n\nPREDICTED:\n\n")
            # print(predicted)



            # assert False





if __name__ == "__main__":
    main()

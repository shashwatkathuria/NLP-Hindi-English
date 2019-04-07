# -*- coding: utf-8 -*-

from __future__ import division
import codecs
from collections import defaultdict

def main():
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")
    calculateEmissionProbabilities(trainFile)

def calculateEmissionProbabilities(trainFile):

    emissionProbabilityDict = defaultdict(int)
    emissionCountDict = defaultdict(int)
    separateTagCountDict = defaultdict(int)
    # Itertaing through the lines of the input file
    for line in trainFile.readlines():

        # Getting tokens form each such line
        tokens = line.split()

        # Initializing a list for the tags observed in the line
        tags = []

        # For each token in that line
        for token in tokens:

                # Extracting the word by splitting and stripping according to the file
                word  = token.split('|')[0].strip()
                # Extracting the tag by splitting and stripping according to the file
                tag = token.split('|')[2].split('.')[0].strip(':?').strip()

                # Giving exact tags in training data a common parent tag for less complexity
                # and more accuracy
                if (tag=='I-NP' or tag=='B-NP' or tag=='O'):
                    tag='NN'

                # Appending the tag to the list of tags
                tags.append(tag)

                # Calculating the number of times the tag and word appear together
                emissionCountDict[tag + '|' + word] += 1

                # Calculating the number of times that tag appears in general
                separateTagCountDict[tag] += 1

    print(separateTagCountDict)

    for key in emissionCountDict:

        tagAndWord = key.split('|')
        tag = tagAndWord[0]
        word = tagAndWord[1]
        emissionProbability = emissionCountDict[tag + '|' + word] / separateTagCountDict[tag]
        emissionProbabilityDict[word + '|' + tag] = emissionProbability

    return emissionProbabilityDict


if __name__ == "__main__":
    main()

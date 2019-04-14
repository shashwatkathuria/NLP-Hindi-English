# -*- coding: utf-8 -*-

from __future__ import division
import codecs
from collections import defaultdict

def main():
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")
    emissionProbabilityDict = calculateEmissionProbabilities(trainFile)
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")
    transitionProbabilityDict, allTags = calculateTransitionProbabilities(trainFile)
    inputSentences = codecs.open("input.txt", mode = "r", encoding = "utf-8")

    sentencesList = []
    for line in inputSentences:
        sentence = []
        tokens = line.split()
        for token in tokens:
            word = token.split('|')[0].strip()
            sentence.append(token)

        sentencesList.append(sentence)

    # print(allTags)

    # for sentence in sentencesList:
    #     for word in sentence:
    #         print word,
    #     print(" ")

    # s = 0
    # for key in emissionProbabilityDict:
    #     print(key,emissionProbabilityDict[key])
    #     s += 1
    #
    # print(s)

    # s = 0
    # for key in transitionProbabilityDict:
    #     if transitionProbabilityDict[key] > 1:
    #         print(key,transitionProbabilityDict[key])
    #     s += 1
    #
    # print(s)
    # viterbiAlgorithm(sentencesList[1], allTags, emissionProbabilityDict, transitionProbabilityDict)

    for sentence in sentencesList:
        viterbiAlgorithm(sentence, allTags, emissionProbabilityDict, transitionProbabilityDict)

def viterbiAlgorithm(sentence, allTags, emissionProbabilityDict, transitionProbabilityDict):

    sentence = [ u'*', u'*' ] + sentence
    initialLength = len(sentence)
    backtrackingDP = defaultdict(list)
    dpDict = {}
    dpDict[0, '*', '*'] = 1

    # print(allTags)
    for u in ([ u'*' ] + list(allTags)):
        for v in ([ u'*' ] + list(allTags)):
            if u != u'*' or v != u'*':
                dpDict[0, u, v] = 1


    tagsAssigned = []
    for k in range(1, initialLength):
        print(" K : " + str(k))
        print(sentence[k])
        for v in allTags:
            for u in allTags:
                possibilities = []
                for w in allTags:
                    # if emissionProbabilityDict[sentence[k] + '|' + v] == 0:
                    #     print("HELLO")
                    #     return
                    possibility = dpDict[k - 1 , w, u] * transitionProbabilityDict[(v, w, u)] * ( 0.000000001 + emissionProbabilityDict[sentence[k] + '|' + v])
                    print(possibility)
                    possibilities.append((possibility, w))

                maxUVgivenK = max(possibilities, key = lambda element:element[0])
                dpDict[k, u, v] = maxUVgivenK[0]
                backtrackW = maxUVgivenK[1]
                backtrackingDP[u, v] += [backtrackW]
                if k == initialLength - 1:
                    backtrackingDP[u, v] += [u, v]
                # print((k, u, v),str(dpDict[k, u, v]))
    # s = 0
    # for key in dpDict:
    #     s += 1
    #     print(key, dpDict[key])
    #
    # print(s)
    # backtrackingDP
    maxPossibilitiesList = []
    s = 0
    for key in dpDict:
        s += 1
        if (initialLength - 1 in key) and dpDict[key]!=0:
            # print(key, dpDict[key])
            maxPossibilitiesList.append((key[1:], dpDict[key]))

    ans = max(maxPossibilitiesList, key = lambda element:element[1])
    # print(ans)
    # print(backtrackingDP[ans[0]][3:])
    print()
    print()
    tagsAssigned = backtrackingDP[ans[0]][3:]
    sentence = sentence[2:]
    print(len(tagsAssigned), len(sentence))
    for i in range(len(sentence)):
        print sentence[i] + " " + tagsAssigned[i],
    # print(s)


def calculateTransitionProbabilities(trainFile):

    transitionProbabilityDict = defaultdict(int)
    trigramTransitionCountDict = defaultdict(int)
    bigramTransitionCountDict = defaultdict(int)
    s = 0
    s1 = 0
    allTags = set([])
    # Iterating through the lines of the input file
    for line in trainFile.readlines():

        # Getting tokens from each such line
        tokens = line.split()

        # Initializing a list for the tags observed in the line
        tags = []

        # For each token in that line
        for token in tokens:

            # Extracting the tag by splitting and stripping according to the file
            tag = token.split('|')[2].split('.')[0].strip(':?').strip()

            # Giving exact tags in training data a common parent tag for less complexity
            # and more accuracy
            if (tag == 'I-NP' or tag == 'B-NP' or tag == 'O'):
                tag = 'NN'

            allTags = allTags | set([tag])

            # Appending the tag to the list of tags
            tags.append(tag)

        s += len(tags)
        # print(tags)

        # If the line read is not a blank line
        if tags != []:
            s1+=1
            # Getting the bigrams in the exact order by zipping through the tags
            bigramSentenceList = zip(tags,tags[1:])

            # Getting the trigrams in the exact order by zipping through the tags
            trigramSentenceList = zip(tags, tags[1:], tags[2:])

            for bigram in bigramSentenceList:
                bigramTransitionCountDict[bigram] += 1


            for trigram in trigramSentenceList:
                trigramTransitionCountDict[trigram] += 1

    # Calculating the transition probabilities finally
    for trigram in trigramTransitionCountDict:
        uvBigram = trigram[:-1]
        sState = (trigram[-1],)
        keySgivenUV = sState + uvBigram

        transitionProbability = (trigramTransitionCountDict[trigram] + 1) / (bigramTransitionCountDict[uvBigram] + 22)

        transitionProbabilityDict[keySgivenUV] = transitionProbability

    # print("----------------------")
    # s = 0
    # for key in transitionProbabilityDict:
    #     s+=1
    #     print(key,transitionProbabilityDict[key])
    print("Number of Words     : " + str(s))
    print("Number of Sentences : " + str(s1))
    return transitionProbabilityDict, allTags


def calculateEmissionProbabilities(trainFile):

    emissionProbabilityDict = defaultdict(int)
    emissionCountDict = defaultdict(int)
    separateTagCountDict = defaultdict(int)

    # Iterating through the lines of the input file
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
                if (tag == 'I-NP' or tag == 'B-NP' or tag == 'O'):
                    tag = 'NN'

                # Appending the tag to the list of tags
                tags.append(tag)

                # Calculating the number of times the tag and word appear together
                emissionCountDict[tag + '|' + word] += 1

                # Calculating the number of times that tag appears in general
                separateTagCountDict[tag] += 1


    for key in emissionCountDict:

        tagAndWord = key.split('|')
        tag = tagAndWord[0]
        word = tagAndWord[1]
        emissionProbability = (emissionCountDict[tag + '|' + word] + 1) / (separateTagCountDict[tag] + 22)
        # print(emissionProbability)
        emissionProbabilityDict[word + '|' + tag] = emissionProbability

    return emissionProbabilityDict


if __name__ == "__main__":
    main()

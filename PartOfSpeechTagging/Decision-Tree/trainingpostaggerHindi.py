# -*- coding: utf-8 -*-

# Importing the libraries required
import nltk, codecs
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

# TRAINING DECISION TREE POS TAGGER IN HINDI USING THE ABOVE LIBRARIES

# Initializing the classifier to be used
classifier = Pipeline([
    ('vectorizer', DictVectorizer(sparse = False)),
    ('classifier', DecisionTreeClassifier(criterion = 'entropy'))
])

def main():

    # Opening training file
    trainFile = codecs.open("trainDataHindi.txt", mode = "r", encoding = "utf-8")

    # Getting the nltk corpus treebank consisting of tagged sentences
    taggedSentences = getTaggedSentences(trainFile)[:-30000]

    # Printing the number of tagged sentences and words in the same
    print("Number of tagged sentences in dataset : " + str(len(taggedSentences)))
    numberOfWords = 0
    for sentence in taggedSentences:
        numberOfWords += len(sentence)

    print("Number of tagged words in dataset     : " + str(numberOfWords))

    # # Printing an example illustrating the features used in the model
    # exampleFeatures = features(['मेरा', 'नाम', 'शाश्वत', 'कथूरिया', 'है', '2011'], 2)
    # for key in exampleFeatures:
    #     print key,
    #     print exampleFeatures[key]

    # Training 75% of tagged sentences as it is an ideal partition
    cutoff = int(.75 * len(taggedSentences))

    # Splitting the same to learn from 75% and then test on 25% of data
    trainingSentences = taggedSentences[:cutoff]
    testSentences = taggedSentences[cutoff:]

    # Printing the number of tagged sentences and test sentences
    print("The number of training sentences are  : " + str(len(trainingSentences)))
    print("The number of test sentences are      : " + str(len(testSentences)))

    # Tranforming to dataset to use inbuilt classifier function to train the model
    X, y = transformToDataset(trainingSentences)

    print("\nPlease wait...Training the model.\n")

    # Training(Fitting) the model
    classifier.fit(X[:10000], y[:10000])

    print("Training completed.")

    # Tranforming to dataset to use inbuilt classifier function to train the model
    XTest, yTest = transformToDataset(testSentences)

    # Computing and printing the accuracy of the model
    print("\n===================\n")
    print("ACCURACY : " + str(classifier.score(XTest, yTest) * 100))
    print("\n===================\n")
    # Opening the input file
    inputSentences = codecs.open("input.txt", mode = "r", encoding = "utf-8")

    # Initializing list for storing input sentences
    sentencesList = []

    # Reading the input file and storing the sentences
    for line in inputSentences:
        sentence = []
        tokens = line.split()
        for token in tokens:
            word = token.split('|')[0].strip()
            sentence.append(token)

        # Appending the sentence in the list of sentences
        sentencesList.append(sentence)

    print("\n===========================\nPRINTING THE RESULTS\n===========================\n")
    # Iterating through each of the sentences
    for sentence in sentencesList:

        # Calling the algorithm on the sentence
        predictedWordsAndTags = posTag(sentence)
        print("\n=======\n")
        # Printing the result of the algorithm
        for (word, tag) in predictedWordsAndTags:
            print word, tag,
        print("\n")
    print("\n=========================\n")

def features(sentence, index):
    """Function to return the features to be used in the model. Index is the index of the specific word in the sentence."""

    # Returning the necessary features applied to the word, i.e., sentence[index]
    return {
        'word': sentence[index],
        'isFirst': index == 0,
        'isLast': index == len(sentence) - 1,
        'prefix1': sentence[index][0],
        'prefix2': sentence[index][:2],
        'prefix3': sentence[index][:3],
        'suffix1': sentence[index][-1],
        'suffix2': sentence[index][-2:],
        'suffix3': sentence[index][-3:],
        'previousWord': '' if index == 0 else sentence[index - 1],
        'nextWord': '' if index == len(sentence) - 1 else sentence[index + 1],
        'hasHyphen': '-' in sentence[index],
        'isNumeric': sentence[index].isdigit()
    }

def untag(taggedSentence):
    """Function to strip the tags from the sentences in our trained corpus and return the list of only words."""
    return [word for word, tag in taggedSentence]


def transformToDataset(taggedSentences):
    """Function to tranform the tagged sentences into dataset suitable to pass into inbuilt classifier function."""
    # X is the list of word specific the features and y is the corresponding tags
    X, y = [], []

    # Appending the corresponding values of features and tags to X and y respectively
    for taggedSentence in taggedSentences:
        untaggedSentence = untag(taggedSentence)
        for index in range(len(taggedSentence)):
            X.append(features(untaggedSentence, index))
            y.append(taggedSentence[index][1])

    return X, y

def posTag(sentence):
    tags = classifier.predict([features(sentence, index) for index in range(len(sentence))])
    return zip(sentence, tags)


def getTaggedSentences(trainFile):
    """Function to get the tagged sentences in the input file. Output is the list of sentences
       with elements as word, tag tuples."""

    # Initializing all tags list as a set
    allTags = set([])

    # Initializing sentences list
    sentencesList = []

    # Iterating through the lines of the input file
    for line in trainFile.readlines():

        # Getting tokens from each such line
        tokens = line.split()

        sentence = []

        # Initializing a list for the tags observed in the line
        tags = []

        # For each token in that line
        for token in tokens:

            word = token.split('|')[0].strip()
            # Extracting the tag by splitting and stripping according to the file
            tag = token.split('|')[2].split('.')[0].strip(':?').strip()

            # Giving exact tags in training data a common parent tag for less complexity
            # and more accuracy
            if (tag == 'I-NP' or tag == 'B-NP' or tag == 'O'):
                tag = 'NN'

            # Appending (word, tag) tuple to the sentence
            sentence.append((word, tag))

            allTags = allTags | set([tag])

            # Appending the tag to the list of tags
            tags.append(tag)

        # Appending the sentence to the list of sentences
        sentencesList.append(sentence)

    return sentencesList

if __name__ == "__main__":
    main()

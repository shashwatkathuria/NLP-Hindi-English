# -*- coding: utf-8 -*-

# Importing the libraries required
import nltk
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

# TRAINING DECISION TREE POS TAGGER IN ENGLISH USING THE ABOVE LIBRARIES

# Initializing the classifier to be used
classifier = Pipeline([
    ('vectorizer', DictVectorizer(sparse = False)),
    ('classifier', DecisionTreeClassifier(criterion = 'entropy'))
])

def main():

    # Getting the nltk corpus treebank consisting of tagged sentences
    taggedSentences = nltk.corpus.treebank.tagged_sents()

    # Printing the number of tagged sentences and words in the same
    print("Number of tagged sentences in dataset : " + str(len(taggedSentences)))
    print("Number of tagged words in dataset     : " + str(len(nltk.corpus.treebank.tagged_words())))

    # # Printing an example illustrating the features used in the model
    # exampleFeatures = features(['This', 'is', 'a', 'sentence'], 2)
    # for key in exampleFeatures:
    #     print key,
    #     print exampleFeatures[key]

    # Training 75% of tagged sentences as it is an ideal partition
    cutoff = int(.75 * len(taggedSentences))

    # Splitting the same to learn from 75% and then test on 25% of data
    trainingSentences = taggedSentences[:cutoff]
    testSentences = taggedSentences[cutoff:]

    # Printing the number of tagged sentences and test sentences
    print("The number of training sentences are : " + str(len(trainingSentences)))
    print("The number of test sentences are     : " + str(len(testSentences)))

    # Tranforming to dataset to use inbuilt classifier function to train the model
    X, y = transformToDataset(trainingSentences)

    print("\nPlease wait...Training the model.\n")

    # Training(Fitting) the model
    classifier.fit(X[:10000], y[:10000])

    print("Training completed.")

    # Tranforming to dataset to use inbuilt classifier function to train the model
    XTest, yTest = transformToDataset(testSentences)

    # Computing and printing the accuracy of the model
    print("\nThe accuracy of the trained model is : " + str(classifier.score(XTest, yTest)))

    # Printing the sentence to be POS tagged
    sentence = "My name is Shashwat Kathuria."
    print("\nTagging the sentence : " + sentence + "\n")

    # Tagging the sentence using the trained model
    print(posTag(nltk.word_tokenize(sentence)))

def features(sentence, index):
    """Function to return the features to be used in the model. Index is the index of the specific word in the sentence."""

    # Returning the necessary features applied to the word, i.e., sentence[index]
    return {
        'word': sentence[index],
        'isFirst': index == 0,
        'isLast': index == len(sentence) - 1,
        'isCapitalized': sentence[index][0].upper() == sentence[index][0],
        'isAllCaps': sentence[index].upper() == sentence[index],
        'isAllLower': sentence[index].lower() == sentence[index],
        'prefix1': sentence[index][0],
        'prefix2': sentence[index][:2],
        'prefix3': sentence[index][:3],
        'suffix1': sentence[index][-1],
        'suffix2': sentence[index][-2:],
        'suffix3': sentence[index][-3:],
        'previousWord': '' if index == 0 else sentence[index - 1],
        'nextWord': '' if index == len(sentence) - 1 else sentence[index + 1],
        'hasHyphen': '-' in sentence[index],
        'isNumeric': sentence[index].isdigit(),
        'capitalsInside': sentence[index][1:].lower() != sentence[index][1:]
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
    """Function to return the tags as predicted by the model."""
    tags = classifier.predict([features(sentence, index) for index in range(len(sentence))])
    return zip(sentence, tags)

if __name__ == "__main__":
    main()

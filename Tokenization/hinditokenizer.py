# -*- coding: utf-8 -*-

# TOKENIZER FOR HINDI LANGUAGE

import re, codecs

def main():
    tokenizer = Tokenizer('''वाशिंगटन: दुनिया के सबसे शक्तिशाली देश के राष्ट्रपति बराक ओबामा ने प्रधानमंत्री नरेंद्र मोदी के संदर्भ में 'टाइम' पत्रिका में लिखा, "नरेंद्र मोदी ने अपने बाल्यकाल में अपने परिवार की सहायता करने के लिए अपने पिता की चाय बेचने में मदद की थी। आज वह दुनिया के सबसे बड़े लोकतंत्र के नेता हैं और गरीबी से प्रधानमंत्री तक की उनकी जिंदगी की कहानी भारत के उदय की गतिशीलता और क्षमता को परिलक्षित करती है।''')
    tokenizer.generateSentences()
    tokenizer.tokenize()
    frequencyDict = tokenizer.generateFrequencyDict()
    s = tokenizer.concordance('बातों')
    frequencyDict = tokenizer.generateStemDict()
    z = tokenizer.removeStopWords()
    tokenizer.printTokens(tokenizer.finalTokens)
    print("The number of sentences are : " + str(tokenizer.sentenceCount()) )
    print("The number of tokens are : " + str(tokenizer.tokensCount()) )
    print("The length of the text is : " + str(tokenizer.textLength()) )

class Tokenizer():

    def __init__(self, text = None):
        if text is not None:
            self.text = text.decode('utf-8')
            self.cleanText()
        else:
            self.text = None
        self.sentences = []
        self.tokens = []
        self.stemmedWords = []
        self.finalList = []

    def readFromFile(self, filename):
        f = codecs.open(filename, encoding = 'utf-8')
        self.text = f.read()
        self.cleanText()

    def generateSentences(self):
        text = self.text
        self.sentences = text.split(u"।")

    def printSentences(self, sentences = None):
        if sentences:
            for i in sentences:
                print(i.encode('utf-8'))
        else:
            for i in self.sentences:
                print(i.encode('utf-8'))

    def cleanText(self):
        text = self.text
        text = re.sub(r'(\d+)',r'',text)
        text = text.replace(u',','')
        text = text.replace(u'"','')
        text = text.replace(u'(','')
        text = text.replace(u')','')
        text = text.replace(u'"','')
        text = text.replace(u':','')
        text = text.replace(u"'",'')
        text = text.replace(u"‘‘",'')
        text = text.replace(u"’’",'')
        text = text.replace(u"''",'')
        text = text.replace(u".",'')
        self.text = text

    def removeOnlySpaceWords(self):
        tokens = filter(lambda tokenizeSpaceWords: tokenizeSpaceWords.strip(),self.tokens)
        self.tokens = tokens

    def hyphenatedTokens(self):
        for each in self.tokens:
            if '-' in each:
                hyphenatedTokenizedWord = each.split('-')
                self.tokens.remove(each)
                self.tokens.append(hyphenatedTokenizedWord[0])
                self.tokens.append(hyphenatedTokenizedWord[1])

    def tokenize(self):
        if not self.sentences:
            self.generateSentences()

        sentencesList = self.sentences
        tokens = []
        for each in sentencesList:
            wordList = each.split(' ')
            tokens = tokens + wordList
        self.tokens = tokens
        self.removeOnlySpaceWords()
        self.hyphenatedTokens()

    def printTokens(self, printList = None):
        if printList is None:
            for i in self.tokens:
                print(i.encode('utf-8'))
        else:
            for i in printList:
                print(i.encode('utf-8'))

    def tokensCount(self):
        return len(self.tokens)

    def sentenceCount(self):
        return len(self.sentences)

    def textLength(self):
        return len(self.text)

    def concordance(self,word):
        if not self.sentences:
            self.generateSentences()

        sentence = self.sentences
        concordanceSent = []
        for each in sentence:
            each = each.encode('utf-8')
            if word in each:
                concordanceSent.append(each.decode('utf-8'))
        return concordanceSent

    def generateFrequencyDict(self):
        freq = {}
        if not self.tokens:
            self.tokenize()

        tempTokens = self.tokens
        for each in self.tokens:
            freq[each] = tempTokens.count(each)

        return freq

    def printFrequencyDict(self, freq):
        for i in freq.keys():
            print(i.encode('utf-8'), ',', freq[i])

    def generateStemWords(self, word):
        suffixes = {
        1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
        2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],
        3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
        4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
        5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"],
        }

        for L in 5,4,3,2,1:
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    if word.endswith(suf):
                        return word[ :-L]

        return word

    def generateStemDict(self):
        stemWord = {}
        if not self.tokens:
            self.tokenize()
        for eachToken in self.tokens:
            temp = self.generateStemWords(eachToken)
            stemWord[eachToken] = temp
            self.stemmedWords.append(temp)

        return stemWord

    def removeStopWords(self):
        f = codecs.open("HindiStopWords.txt", encoding = 'utf-8')
        if not self.stemmedWords:
            self.generateStemDict()
        stopwords = [x.strip() for x in f.readlines()]
        tokens = [i for i in self.stemmedWords if unicode(i) not in stopwords]
        self.finalTokens = tokens
        return tokens

if __name__ == "__main__":
    main()

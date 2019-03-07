from  nltk.tokenize import sent_tokenize, word_tokenize

# NATURAL LANGUAGE PROCESSING - TOKENIZATION

def main():

    example_text = "Hello Mr. Singh, how are you doing today? The weather is great and everything seems so nice. I am going to play. My friends are waiting for me outside."
    tokenizeNLP(example_text)


def tokenizeNLP(text):

    print("\nTokenizing into sentences : \n")
    for sentence in sent_tokenize(text):
        print(sentence)

    print("\nTokenizing into words : \n")
    for word in word_tokenize(text):
        print(word)

if __name__=="__main__":
    main()

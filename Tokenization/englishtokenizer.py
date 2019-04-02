from  nltk.tokenize import sent_tokenize, word_tokenize

# TOKENIZER FOR ENGLISH LANGUAGE

def main():

    example_text = "1066 In this year the monastery at Westminster was hallowed on Childermas day (28 December). And king Eadward died on Twelfth-mass eve (5 January) and he was buried on Twelfth-mass day, in the newly hallowed church at Westminster. And earl Harold succeeded to the Kingdom of England, as the king had granted it to him and men had also chosen him thereto and he was blessed as king on Twelfth-mass day. And in the same year that he was king he went out with a naval force against William ... And the while count William landed at Hastings, on St. Michael's mass-day and Harold came from the north and fought against him before his army had all come and there he fell and his two brothers Gyrth and Leofwine and William subdued this land, and came to Westminster and archbishop Ealdred hallowed him king and men paid him tribute and gave him hostages and afterwards bought their land"
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

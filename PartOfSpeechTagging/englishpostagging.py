import nltk

# ENGLISH POS TAGGER

sampleText = "After hearing what both had to say, I briefly told them--That it had been the earnest wish of governmt. to bring the people of those counties to a sense of their duty, by mild, & lenient means; That for the purpose of representing to their sober reflection the fatal consequences of such conduct Commissioners had been sent amongst them that they might be warned, in time, of what must follow, if they persevered in their opposition to the laws; but that coercion wou'd not be resorted to except in the dernier resort: but, that the season of the year made it indispensible that preparation for it should keep pace with the propositions that had been made; That it was unnecessary for me to enumerate the transactions of those people (as they related to the proceedings of government) forasmuch as they knew them as well as I did; That the measure which they were not witness to the adoption of was not less painful than expensive--Was inconvenient, & distressing--in every point of view; but as I considered the support of the Laws as an object of the first magnitude, and the greatest part of the expense had already been incurred, that nothing Short of the most unequivocal proofs of absolute Submission should retard the March of the army into the Western counties, in order to convince them that the government could, & would enforce obedience to the laws--not suffering them to be insulted with impunity. Being asked again what proofs would be required, I answered, they knew as well as I did, what was due to justice & example. They understood my meaning--and asked if they might have another interview. I appointed five oclock in the After noon for it. At this second Meeting there was little more than a repeti[ti]on of what had passed in the forenoon; and it being again mentioned that all the principal characters, except one, in the Western counties who had been in the opposition, had submitted to the propositions--I was induced, seeing them in the Street the next day, to ask Mr. Redick who that one was?--telling him at the same time I required no disclosure that he did not feel himself entirely free to make. He requested a little time to think of it, and asked for another meeting--which was appointed at 5 oclock that afternoon--which took place accordingly when he said David Bradford was the person he had alluded to in his former conversations."

def main():
    tagsAndTokens = nltk.pos_tag(nltk.word_tokenize(sampleText))

    for tagAndToken in tagsAndTokens:
        print("Tag : " + tagAndToken[0])
        print("Token : " + tagAndToken[1] + "\n")

if __name__ == "__main__":
    main()

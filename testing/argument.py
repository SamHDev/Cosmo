input_text = "how do you spell London Bridge"

import re

intents = []

import difflib


def similar(a, b): return difflib.SequenceMatcher(None, a, b).ratio()


class Intent:
    def __init__(self):
        self.phrases = []
        self.arguments = []

# regex, Allow Multiple
def word():
    return r"([a-zA-Z]*)", True


intents.append(Intent())
intents[0].arguments.append(["word", word()])
intents[0].phrases.append("how do you spell {word}")
intents[0].phrases.append("spell {word}")

intents.append(Intent())
intents[1].arguments.append(["word", word()])
intents[1].phrases.append("what does the word {word} mean")
intents[1].phrases.append("define {word}")

query = input_text
query_words = query.lower().split(" ")
similar_threshold = 0.9

for intent in intents:
    for phrase in intent.phrases:
        score = 0
        score_max = len(query_words)
        phrase_query_words = query_words.copy()
        phrase_arguments = {}
        for argname in re.compile(r"{(.*)}").findall(phrase):
            phrase_arguments[argname[0]] = []
        for phrase_word in phrase.lower().split(" "):
            phrase_args = re.compile(r"{(.*)}").findall(phrase_word)
            phrase_arg = (len(phrase_args) != 0)
            if phrase_arg:
                phrase_argname = phrase_args[0][0]
            else:
                phrase_argname = None
            for query_word in phrase_query_words:
                #print(query_word,phrase_query_words)
                similar_result = similar(query_word, phrase_word)
                if similar_result >= similar_threshold:
                    score = score + 1
                    for query2 in phrase_query_words:
                        phrase_query_words.pop(0)
                        if query2 == query_word:
                            break
                    break
                else:
                    if (phrase_arg):
                        phrase_arguments[phrase_argname].append(query_word)
                        score = score + 1
                        #phrase_query_words.remove(query_word)
        print(phrase, score / score_max, score, score_max,phrase_arguments)

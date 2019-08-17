input_text = "how do you spell London"

import re

intents = []

import difflib


def similar(a, b): return difflib.SequenceMatcher(None, a, b).ratio()


class Intent:
    def __init__(self):
        self.phrases = []
        self.arguments = []


def word():
    return r"([a-zA-Z]*)"


intents.append(Intent())
intents[0].arguments.append(["word", word()])
intents[0].phrases.append("how do you spell {word}")
intents[0].phrases.append("spell {word}")

query = input_text
query_words = query.lower().split(" ")
similar_threshold = 0.9

for intent in intents:
    for phrase in intent.phrases:
        score = 0
        score_max = len(query_words)
        phrase_arguments = {}
        for argname in re.compile(r"{(.*)}").findall(phrase)
            phrase_arguments[argname] = []
        for phrase_word in phrase.lower().split(" "):
            phrase_args = re.compile(r"{(.*)}").findall(phrase_word)
            phrase_arg = (len(phrase_args) != 0)
            if phrase_arg:
                phrase_argname = phrase_args[0][0]
            else:
                phrase_argname = None
            for query_word in query_words:
                similar_result = similar(query_word, phrase_word)
                if similar_result >= similar_threshold:
                    print("MATCHING WORD", query_word)
                    score = score + 1
                    query_words.remove(query_word)
                    break
                else:
                    phrase_arg
        print(phrase, score / score_max, score, score_max)

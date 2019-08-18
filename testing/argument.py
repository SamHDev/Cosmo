input_text = "how do you spell London Bridge"

input_text = "set value name to 10"

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


def number():
    return r"([0-9]*)", False


intents.append(Intent())
intents[0].arguments.append(["word", word()])
intents[0].phrases.append("how do you spell {word}")
intents[0].phrases.append("spell {word}")

intents.append(Intent())
intents[1].arguments.append(["word", word()])
intents[1].phrases.append("what does the word {word} mean")
intents[1].phrases.append("define {word}")

intents.append(Intent())
intents[2].arguments.append(["word", word()])
intents[2].arguments.append(["number", number()])
intents[2].phrases.append("set value {word} to {number}")
intents[2].phrases.append("change value {word} to {number}")

query = input_text
query_words = query.lower().split(" ")
similar_threshold = 0.9

for intent in intents:
    for phrase in intent.phrases:
        score = 0
        phrase_query_words = query_words.copy()
        phrase_arguments = {}
        for argname in re.compile(r'\{(.+?)\}').findall(phrase):
            phrase_arguments[argname] = []
        print(phrase_arguments)
        for phrase_word in phrase.lower().split(" "):
            phrase_args = re.compile(r'\{(.+?)\}').findall(phrase_word)
            phrase_arg = (len(phrase_args) != 0)
            if phrase_arg:
                phrase_argname = phrase_args[0]
            else:
                phrase_argname = None
            for query_word in phrase_query_words:
                # print(query_word,phrase_query_words)
                similar_result = similar(query_word, phrase_word)
                if similar_result >= similar_threshold:
                    score = score + 1
                    # print(query_word,phrase_word, phrase_query_words, score)
                    for i in range(0, phrase_query_words.index(query_word) + 1):
                        phrase_query_words.pop(0)
                    break
                elif phrase_arg:
                    found_argument = None
                    for finder_arg in intent.arguments:
                        if finder_arg[0] == phrase_argname:
                            found_argument = finder_arg
                    if len(re.compile(found_argument[1][0]).findall(query_word)) != 0:
                        phrase_arguments[phrase_argname].append(query_word)
                        score = score + 0.75
                        print(query_word, phrase_word, phrase_query_words, score)
                        if found_argument[1][1] == False:
                            phrase_query_words.remove(query_word)
                    else:
                        score = score + 0.25
                else:
                    score = score - 0.55

        print(phrase, score, phrase_arguments)
        print("-" * 50)

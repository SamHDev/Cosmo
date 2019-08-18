# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

# Text Input
input_text = "how do you spell London Bridge"
input_text = "set value name to 10"

import re
import difflib

intents = []


# Sim Ratio Function
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


#intents.append(Intent())
#intents[0].arguments.append(["word", word()])
#intents[0].phrases.append("how do you spell {word}")
#intents[0].phrases.append("spell {word}")

#intents.append(Intent())
#intents[1].arguments.append(["word", word()])
#intents[1].phrases.append("what does the word {word} mean")
#intents[1].phrases.append("define {word}")

intents.append(Intent())
intents[0].arguments.append(["word", word()])
intents[0].arguments.append(["number", number()])
intents[0].phrases.append("set value {word} to {number}")
#intents[2].phrases.append("change value {word} to {number}")

query = input_text
query_words = query.lower().split(" ")
similar_threshold = 0.9

# Loop Through Intents
for intent in intents:
    # Loop Through Phrases
    for phrase in intent.phrases:

        # Create our per phrase vars
        score = 0  # Score to Keep Track and Evaluate the Best Phrase
        phrase_query_words = query_words.copy()  # Create a copy of the query list
        phrase_arguments = {}  # Blank Dict to store argument values we find
        phrase_matched_words = []  # Matched words we find

        # Finding Phrase Matched Words for use in argument finding
        for phrase_word in phrase.lower().split(" "):  # Loop Over each word in phrase
            # Find Arguments in word
            phrase_args = re.compile(r'\{(.+?)\}').findall(phrase_word)
            phrase_arg = (len(phrase_args) != 0)

            # Loop through query words
            for query_word in phrase_query_words:
                if not phrase_arg:  # If not argument
                    # Check Similarity
                    similar_result = similar(query_word, phrase_word)
                    if similar_result >= similar_threshold:
                        phrase_matched_words.append(query_word)  # Add word to our matched list
                        # print(query_word,phrase_word, phrase_query_words, score)

        # Create blank lists in our blank dict for each argument name found in the intent
        for argname in re.compile(r'\{(.+?)\}').findall(phrase):
            phrase_arguments[argname] = []
        print(phrase_arguments)
        print(phrase_matched_words)

        # Recopy that list
        phrase_query_words = query_words.copy()

        #Loop Through Each Word in The Phrase
        for phrase_word in phrase.lower().split(" "):
            next_word = False
            phrase_args = re.compile(r'\{(.+?)\}').findall(phrase_word)
            phrase_arg = (len(phrase_args) != 0)
            if phrase_arg:
                phrase_argname = phrase_args[0]
            else:
                phrase_argname = None
            for query_word in phrase_query_words:
                print(phrase_word, " | ", query_word, " | ", phrase_query_words, " | ", phrase_matched_words, " | ",
                      phrase_arguments, " | ", score)
                similar_result = similar(query_word, phrase_word)
                if similar_result >= similar_threshold:
                    score = score + 1
                    # print(query_word,phrase_word, phrase_query_words, score)
                    for i in range(0, phrase_query_words.index(query_word) + 1):
                        phrase_query_words.pop(0)
                    continue
                elif phrase_arg:
                    if query_word in phrase_matched_words:
                        print(query_word)
                        phrase_query_words.remove(query_word)
                        score = score + 0.1
                        next_word = True
                        break
                    else:
                        found_argument = None
                        for finder_arg in intent.arguments:
                            if finder_arg[0] == phrase_argname:
                                found_argument = finder_arg
                        if len(re.compile(found_argument[1][0]).findall(query_word)) != 0:
                            phrase_arguments[phrase_argname].append(query_word)
                            score = score + 0.75
                            # print(query_word, phrase_word, phrase_query_words, score)
                            if found_argument[1][1] == False:
                                phrase_query_words.remove(query_word)
                        else:
                            score = score + 0.25
                else:
                    score = score - 0.55

        print(phrase, score, phrase_arguments)
        print("-" * 50)

import re
import difflib


# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

class Intent:
    def __init__(self):
        self.phrases = []
        self.arguments = []


class IntentArgument:
    def __init__(self, name, atype):
        self.name = name
        self.atype = atype


class IntentArgumentType:
    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def get_regex(self):
        return re.compile(self.regex)


# Sim Ratio Function
def similar(a, b): return difflib.SequenceMatcher(None, a, b).ratio()


def similar_check(a, b, thresh):
    return similar(a, b) >= thresh

def similar_check_wres(a, b, thresh):
    check = similar(a, b)
    return check >= thresh, check

def similar_check_list(a, blist, thresh):
    for b in blist:
        if similar_check(a, b, thresh=thresh):
            return True, a, b
    return False, a, None


def get_args(value):
    return re.compile("\{([a-zA-Z0-9]+?)\}").findall(value)


def is_arg(value):
    return len(get_args(value)) != 0


def group_matchs(a_words, b_words, thresh):
    # Copy to not affect anything
    a_words = a_words.copy()
    b_words = b_words.copy()

    # Create Grouping Temp Variables
    grouping = []
    current_grouping = []
    last_group_result = None

    # Loop Over each Query Word:
    for a_word in a_words:
        found, a, b = similar_check_list(a_word, b_words, thresh)  # Check Sim Ratio

        # Fix First Instance Issue (if None)
        if last_group_result is None:
            last_group_result = found

        if last_group_result != found:  # If Found State Changes
            grouping.append([current_grouping, last_group_result])  # Add Working Group to Group list
            current_grouping = []  # Clear List
            last_group_result = found  # Set New State
        current_grouping.append(a)  # Add Item to Working Group

    grouping.append([current_grouping, last_group_result])  # Add Last Group to Phrase Group List

    return grouping


def find_word_in_group(term, groups, thresh):
    groups_count = 0
    for group in groups:
        word_count = 0
        for group_word in group[0]:
            if similar_check(term, group_word, thresh):
                return [True, [term, group_word], [groups_count, word_count]]
            word_count = word_count + 1
        groups_count = groups_count + 1
    return [False, [term, None], None]

def find_middle(location1,location2,grouping):
    pass

def find_intent(intents, query, s_threshold=0.8):
    query_words = query.lower().split(" ")
    for intent in intents:  # Loop Through Intents
        for phrase in intent.phrases:  # Loop Through Phrases:

            # Find Arguments
            arguments = re.compile("\{([a-zA-Z0-9]+?)\}").findall(phrase)
            found_arguments = {}
            for intent_phrase in intent.arguments:
                found_arguments[intent_phrase.name] = []

            # Create Grouping Temp Variables
            phrase_words = phrase.lower().split(" ")

            #
            grouping_a = group_matchs(query_words, phrase_words, s_threshold)
            grouping_b = group_matchs(phrase_words, query_words, s_threshold)

            grouping_matrix = None
            for group_b in grouping_b:
                if group_b[1] == True:
                    for word in group_b[0]:
                        print(find_word_in_group(word, grouping_a, s_threshold))
                else:
                    if is_arg(group_b[0][0]):
                        print("Argument: " + group_b[0][0])
                    else:
                        print("NO FOUND")


# Demo Stuff

string = IntentArgumentType("String", r"([a-zA-Z0-9]*)")

intent_list = []

intent = Intent()
intent.phrases.append("whats the time in {city} along {city2}")
# intent.phrases.append("what time is it in {city} along {city2}")
intent.arguments.append(IntentArgument("city", string))
intent.arguments.append(IntentArgument("city2", string))

intent_list.append(intent)

find_intent(intent_list, "whats the time cosmo in London Bridge along epic gamer")

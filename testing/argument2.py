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


def similar_check_list(a, blist, thresh):
    for b in blist:
        if similar_check(a, b, thresh=thresh):
            return True, a, b
    return False, a, None


def find_intent(intents, query, s_threshold=0.8):
    query_words = query.lower().split(" ")
    for intent in intents:  # Loop Through Intents
        for phrase in intent.phrases:  # Loop Through Phrases:

            # Create Grouping Temp Variables
            grouping = []
            current_grouping = []
            last_group_result = None

            # Loop Over each Query Word:
            for query_word in query_words:
                found, a, b = similar_check_list(query_word, phrase.lower().split(" "), s_threshold)  # Check Sim Ratio

                # Fix First Instance Issue (if None)
                if last_group_result is None:
                    last_group_result = found

                if last_group_result != found:  # If Found State Changes
                    grouping.append([current_grouping, last_group_result]) # Add Working Group to Group list
                    current_grouping = []
                    last_group_result = found
                current_grouping.append(a)

            grouping.append([current_grouping, last_group_result])

            print(grouping)


string = IntentArgumentType("String", r"([a-zA-Z0-9]*)")

intent_list = []

intent = Intent()
intent.phrases.append("whats the time in {city} along {city2}")
intent.phrases.append("what time is it in {city} along {city2}")
intent.arguments.append(IntentArgument("city", string))
intent.arguments.append(IntentArgument("city2", string))

intent_list.append(intent)

find_intent(intent_list, "whats the time in London Bridge along epic gamer")

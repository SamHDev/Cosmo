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

    def find_argument(self, name):
        for arg in self.arguments:
            if name == arg.name:
                return arg
        return None


class IntentArgument:
    def __init__(self, name, atype):
        self.name = name
        self.atype = atype


class IntentArgumentType:
    def __init__(self, name):
        self.name = name

    def check(self, query):
        return True


def IntentArgumentTypeFromRegex(name, regex):
    class SubIntentArgument(IntentArgumentType):
        def __init__(self):
            IntentArgumentType.__init__(self, name)
            self.regex = regex

        def get_regex(self):
            return re.compile(self.regex)

        def check(self, query):
            return len(self.get_regex().findall(query)) != 0

    return SubIntentArgument()


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


def find_middle(loc1, loc2, groups):
    middle = []
    loc = [0, 0]
    for group in groups:
        loc[1] = 0
        for group_word in group[0]:
            if loc1[0] == loc2[0]:
                if loc1[1] < loc[1] < loc2[1]:
                    middle.append(loc.copy())
            else:
                if loc1[0] == loc[0]:
                    if loc1[1] < loc[1]:
                        middle.append(loc.copy())
                elif loc2[0] == loc[0]:
                    if loc2[1] > loc[1]:
                        middle.append(loc.copy())
                elif loc1[0] < loc[0] < loc2[0]:
                    middle.append(loc.copy())

            loc[1] += 1
        loc[0] += 1
    return middle


def find_last(groups):
    grp = len(groups) - 1
    return [grp, len(groups[grp][0]) - 1]


def find_last_own(groups):
    grp = len(groups) - 1
    return [grp, 0]


def find_search(intent, phrase, query, thresh):
    query_words = query.lower().split(" ")

    # Find Arguments
    arguments = re.compile("\{([a-zA-Z0-9]+?)\}").findall(phrase)
    found_arguments = {}
    for intent_phrase in intent.arguments:
        found_arguments[intent_phrase.name] = []

    # Create Grouping Temp Variables
    phrase_words = phrase.lower().split(" ")

    # Find Argument and Phrase Groups
    grouping_a = group_matchs(query_words, phrase_words, thresh)
    grouping_b = group_matchs(phrase_words, query_words, thresh)

    # Arguments for Finding Arguments and Resolving Middle Group
    last_pos = [0, 0]
    argument_name = None
    arguments_find = {}
    score = 0  # Score Var

    # Loop Through Grouping
    for group_b in grouping_b:  # All Groups
        if group_b[1]:  # If Group Is Matched Group
            for word in group_b[0]:  # Sub Groups
                match_place = find_word_in_group(word, grouping_a, thresh)  # Find Location of word (Buggy)
                found = find_middle(last_pos, match_place[2], grouping_a)  # Find Middle Arguments
                # print(found)
                if len(found) != 0:  # If sub groups in middle
                    if argument_name is not None:
                        if argument_name in arguments_find.keys():
                            arguments_find[argument_name] += found
                            score += 0.35  # Add Second Weight
                        else:
                            arguments_find[argument_name] = found
                            score += 0.5  # Add Weight
                else:
                    argument_name = None  # Reset Argument Name
                    score += 1.5  # Base Weight

                last_pos = match_place[2]  # Set last pos
        else:  # If Group Is Non Matched Group
            if is_arg(group_b[0][0]):  # If The Sub Group Word is an argument
                argument_name = get_args(group_b[0][0])[0]  # Get Argument Name with handy dandy argument
                score += 0.5  # Add Argument Filler Weight
            else:
                pass  # Not Found.

    # Last Loop (To catch arguments at end of phrase)
    last_loc = find_last(grouping_a)
    last_loc[1] += 1
    found = find_middle(last_pos, last_loc, grouping_a)  # Find Location of word (Still Buggy)
    # print(found)
    if len(found) != 0:  # If sub groups in middle
        if argument_name is not None:
            if argument_name in arguments_find.keys():
                arguments_find[argument_name] += found
            else:
                arguments_find[argument_name] = found
    else:
        argument_name = None

    # Resolve Argument Words
    argument_data = {}
    for arg_name in arguments_find:  # Loop Through Arguments
        arg_data = []
        for arg_loc in arguments_find[arg_name]:  # Loop Through Sub groups
            arg_data.append(grouping_a[arg_loc[0]][0][arg_loc[1]])  # Add with messy line of code

        if len(arg_data) == 0:
            score -= 1

        arg_data = " ".join(arg_data)  # Join words (with spaces)
        arg = intent.find_argument(arg_name)

        # Check Arg Types
        if arg.atype.check(arg_data):
            score += 0.25  # Add Argument Filler Weight
        else:
            score -= 1  # Add Argument Filler Weight
        argument_data[arg_name] = arg_data

    # Finish Up
    score = round(score, 4)
    return score, argument_data


def find_intent(intents, query, s_threshold=0.8, r_threshold=4):
    results = []  # Results Var

    for intent in intents:  # Loop Through Intents
        for phrase in intent.phrases:  # Loop Through Phrases

            # Search
            score, args = find_search(intent, phrase, query, s_threshold)
            results.append([score, intent, phrase, args])

    # Search Through All Results
    best = [0, None, None, {}]
    for res in results:
        if res[0] > best[0]:
            best = res

    if best[0] < r_threshold:
        return False, None, best[0], None

    # Return (Intent,Score,Args)
    # print(best)
    return True, best[1], best[0], best[3]


# Demo Stuff

string = IntentArgumentTypeFromRegex("String", r"([a-zA-Z0-9]*)")

intent_list = []

intent = Intent()
intent.phrases.append("whats the time in {city} along {city2}")
intent.phrases.append("what time is it in {city} along {city2}")
intent.arguments.append(IntentArgument("city", string))
intent.arguments.append(IntentArgument("city2", string))

intent_list.append(intent)

print(find_intent(intent_list, "whats the time in London Bridge along epic gamer"))

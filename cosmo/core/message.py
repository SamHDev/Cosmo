from difflib import SequenceMatcher
import re


# Similarity Ratio Checker (Quick Fix)
def similar(a, b): return SequenceMatcher(None, a, b).ratio()


# Search Through all Intents and Phrases for our Query (Quick Fix)
def find_intent(cosmo, query, threshold=0.8):
    # Create vars to store best value.
    best_value = threshold
    best_intent = None

    # Loop Through Each Skill
    for skill in cosmo.skills:
        # Loop Through Each Intent
        for intent in skill.intents:
            # Loop Through Each Phrase
            for phrase in intent.phrases:
                # Check the Similarity between the phrase and query.
                value = similar(phrase.text.lower(), query.lower())

                # debug print
                # print(intent.phrases[0].text,": " ,phrase.text, value)

                # Compare Best Value if so replace.
                if value > best_value:
                    best_value = value
                    best_intent = intent

    # Return None if none found
    return best_intent


# Working on Somthing to Include Argsuments in Removal of Gleb's Code.
def find_intent2(cosmo, query, threshold=0.8):
    best_value = threshold
    best_intent = None
    for skill in cosmo.skills:
        for intent in skill.intents:
            for phrase in intent.phrases:
                value = similar(phrase.text.lower(), query.lower())
                # print(intent.phrases[0].text,": " ,phrase.text, value)
                if value > best_value:
                    best_value = value
                    best_intent = intent

    return best_intent


# Just Execute the Intent, and 'catch' the error if 'None' Passed.
def execute_intent(cosmo, intent):
    if intent is None:
        return False
    intent.invoke(cosmo, None)
    return True


# Working on New Message Class to replace Gleb's
class Message:
    pass

# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

import random, re
from .argtypes import ArgumentType
from .argtypes import ArgumentTypeError


class IntentClass:
    def __init__(self, api):
        self.api = api

    def __call__(self, **kwargs):
        return Intent(api=self.api, **kwargs)


# Intent Wrapper
class Intent:
    def __init__(self, api, skill, phrases=(), custom_argument_types=None):
        # Base shit to store more shit
        self.api = api
        self.skill = skill
        self.phrases = []
        self.arguments = []
        for phrase in phrases:
            self.add_phrase(phrase, custom_argument_types)

        self.callbacks = []
        self.callbacks_random = True

    # For Overwrite
    def setup(self):
        pass

    # Add Phrases, Arguments and Callbacks
    def add_phrase(self, phrase_name: str, custom_argument_types=None, allow_hardcode=True):
        if not phrase_name in self.api.phrases.keys():
            if allow_hardcode == False:
                raise PhraseNotFoundError(phrase_name)
            text = phrase_name
        else:
            text = self.api.phrases[phrase_name]

        self.phrases.append(IntentPhrase(text))
        for arg in re.findall(r"(?:\{([a-zA-Z0-9]+)(?:\:([a-zA-Z0-9]+))?(?:\:([a-zA-Z0-9\"]+))?\}(\!?))", text):
            # Get class of argument type
            if arg[1] in dir(ArgumentType) or arg[1] == "":
                argtype = getattr(ArgumentType, (arg[1] if arg[1] != "" else "String"))  # Default type is string
            elif arg[1] in dir(custom_argument_types):
                argtype = getattr(custom_argument_types, arg[1])
            else:
                raise ArgumentTypeError
            # Get default value
            try:
                default = eval(arg[2])
            except:
                default = None

            self.add_argument(name=arg[0], atype=argtype, default=default, required=arg[3] == "!")

    def add_argument(self, name, atype, default=None, required=False):
        self.arguments.append(IntentArgument(name, atype, default, required))

    def add_callback(self, func):
        self.callbacks.append(func)

    def __call__(self, func):
        self.add_callback(func)
        return self  # This is a decorator to make making intents a lot shorter, so it has to return something (the intent with the method set as a callback)

    # INVOKE THE FUCKING INTENT BITCHES
    def invoke(self, cosmo, *args, **kwargs):
        # RANDOM CALLBACK SHIT
        if self.callbacks_random:
            random.choice(self.callbacks)(*args, **kwargs)
        else:
            for callback in self.callbacks:
                callback(*args, **kwargs)


# INTENT PHRASE STORE
class IntentPhrase:
    def __init__(self, text):
        self.text = text


# Self-explanatory
class PhraseNotFoundError(Exception):
    pass


# INTENT ARGUMENT STORE
class IntentArgument:
    def __init__(self, name, atype, default, required):
        self.name = name
        self.atype = atype
        self.default = default
        self.required = required

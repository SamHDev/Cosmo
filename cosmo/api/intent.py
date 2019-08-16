import random


# Intent Wrapper
class Intent:
    def __init__(self):
        # Base shit to store more shit
        self.phrases = []
        self.arguments = []
        self.callbacks = []

        self.callbacks_random = True

    # dunno what this is for
    def setup(self):
        pass

    # Add Phrases, Arguments and Callbacks
    def add_phrase(self, phrase):
        self.phrases.append(IntentPhrase(phrase))

    def add_argument(self, name, atype, default=False, required=False):
        self.arguments.append(IntentArgument(name, atype, default, required))

    def add_callback(self, func):
        self.callbacks.append(func)

    # Add Callback Wrapper to make it look nice than glebs.
    def callback(self, func):
        self.add_callback(func)

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


# INTENT ARGUMENT STORE
class IntentArgument:
    def __init__(self, name, atype, default, required):
        self.name = name
        self.atype = atype
        self.default = default
        self.required = required

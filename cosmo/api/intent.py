

import random, re
from .argtypes import ArgumentType
from .argtypes import ArgumentTypeError

from functools import partial, wraps


def getIntentHandler(api):
    from functools import wraps

    def decorator(*in_args, **in_kwargs):
        def inner_function(function):
            intent = Intent(api, *in_args, **in_kwargs)
            intent.add_callback(function)
            api.api_skill.register_intent(intent)

            return intent
            ''' # Sam's stuff
            @wraps(function)
            def wrapper(*args, **kwargs):
                function(*args, **kwargs)

            return wrapper
            '''
        return inner_function

    return decorator


# Intent Wrapper
class Intent:
    def __init__(self, api, phrases=[], custom_argument_types=None, arguments={}):
        # Base shit to store more shit
        self.skill = None
        self.api = api
        self.phrases = []
        self.arguments = []
        for phrase in phrases:
            self.add_phrases(phrase, custom_argument_types)
        for arg in arguments:
            self.arguments.append(IntentArgument(arg, arguments[arg], None, False))
        self.callbacks = []
        self.callbacks_random = True

    def set_skill(self,skill):
        self.skill = skill

    # For Overwrite
    def setup(self):
        pass

    # Add Phrases, Arguments and Callbacks
    def add_raw_phrase(self, phrase: str, custom_argument_types=None):
        self.phrases.append(IntentPhrase(phrase))
        for arg in re.findall(r"(?:\{([a-zA-Z0-9]+)(?:\:([a-zA-Z0-9]+))?(?:\:([a-zA-Z0-9\"]+))?\}(\!?))", phrase):
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


    def add_phrases(self, phrase_name: str, custom_argument_types=None):
        if not phrase_name in self.api.phrases:
            raise PhraseNotFoundError(phrase_name)
        else:
            texts = self.api.phrases[phrase_name]
        for text in texts:
            self.add_raw_phrase(text, custom_argument_types)

    def add_argument(self, name, atype, default=None, required=False):
        self.arguments.append(IntentArgument(name, atype, default, required))

    def add_callback(self, func):
        self.callbacks.append(func)

    def __call__(self, cosmo, *args, **kwargs):
        self.invoke(cosmo, *args, **kwargs)

    # INVOKE THE FUCKING INTENT BITCHES
    def invoke(self, cosmo, message):
        #print(cosmo,*args,**kwargs)
        # RANDOM CALLBACK SHIT
        if self.callbacks_random:
            random.choice(self.callbacks)(self.skill, cosmo, message)
        else:
            for callback in self.callbacks:
                callback(self.skill, cosmo, message)


    def find_argument(self, name):
        for arg in self.arguments:
            if name == arg.name:
                return arg
        return None


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
        self.atype = atype()
        self.default = default
        self.required = required

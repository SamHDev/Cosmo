

import re


# Argument Type Shit

# Base the IntentArgumentType
class IntentArgument:
    def __init__(self, name, atype):
        self.name = name
        self.atype = atype


class IntentArgumentType:
    def __init__(self, name):
        self.name = name

    def check(self, query):
        return True, False


class IntentArgumentTypeFromRegex(IntentArgumentType):
    def __init__(self, name, regex, caster):
        IntentArgumentType.__init__(self, name)
        self.regex = regex
        self.caster = caster

    def get_regex(self):
        return re.compile(self.regex)


    def check(self, query):
        # print(self.get_regex().findall(query))
        return len(self.get_regex().findall(query)) == 1, self.caster(query)

# Error if argumenttype is not found
class ArgumentTypeError(Exception):
    pass
    
# Argument Type List
class ArgumentType:
    class Word(IntentArgumentTypeFromRegex):
        def __init__(self):
            super().__init__("Word", r"([a-zA-Z]+)}", str)

    class String(IntentArgumentTypeFromRegex):
        def __init__(self):
            super().__init__("Word", r"([a-zA-Z ]+)}", str)

    class Any(IntentArgumentTypeFromRegex):
        def __init__(self):
            super().__init__("Word", r"([.]*)}", str)

    class Int(IntentArgumentTypeFromRegex):
        def __init__(self):
            super().__init__("Word", r"([0-9]{0,})}", int)

    class Float(IntentArgumentTypeFromRegex):
        def __init__(self):
            super().__init__("Word", r"([0-9\.]{0,})}", float)

    class Boolean(IntentArgumentType):
        def check(self, value):
            v = value.lower()
            if v in ["on", "true", "enabled", "yes", "enable"]:
                return True, True
            elif v in ["off", "false", "disabled", "no", "disable"]:
                return True, False
            else:
                return False, None
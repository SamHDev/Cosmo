# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import re

# Argument Type Shit
# This is testing, not implemented just trying out some snytax and shit

# Base the IntentArgumentType
class IntentArgumentType:
    def __init__(self):
        pass

    def check(self, value):
        return None, None

    @staticmethod
    def test_regex(regex, value):
        search = re.compile(regex).findall(value)
        if len(search) == 1:
            return True, search[0][0]
        else:
            return False, None

# Argument Type List
class ArgumentType:
    class Word(IntentArgumentType):
        def check(self, value):
            return self.test_regex(r"([a-zA-Z]{0,})}", value)

    class String(IntentArgumentType):
        def check(self, value):
            return self.test_regex(r"([a-zA-Z ]{0,})}", value)

    class Any(IntentArgumentType):
        def check(self, value):
            return self.test_regex(r"([.]{0,})}", value)

    class Int(IntentArgumentType):
        def check(self, value):
            success, value = self.test_regex(r"([0-9]{0,})}", value)
            if success:
                return success, int(value)
            else:
                return success, value

    class Float(IntentArgumentType):
        def check(self, value):
            success, value = self.test_regex(r"([0-9\.]{0,})}", value)
            if success:
                return success, float(value)
            else:
                return success, value

    class Boolean(IntentArgumentType):
        def check(self, value):
            v = value.lower()
            if v in ["on", "true", "enabled", "yes", "enable"]:
                return True, True
            elif v in ["off", "false", "disabled", "no", "disable"]:
                return True, False
            else:
                return False, None

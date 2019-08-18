# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

from . import intent

# Skill Wrapper
class Skill:
    def __init__(self):
        self.intents = []

    def register_intent(self, intent):
        self.intents.append(intent)

    # Just an Idea (Failed) VERY BIG FAILED
    def find_intents(self):
        for var in dir(self):
            if isinstance(getattr(self, var), intent.Intent):
                self.intents.append(var)

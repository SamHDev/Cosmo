# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import random

# Demo Actions API
class Actions:
    def __init__(self, api):
        self.api = api

    def speak(self, text):
        print(">> " + text)
        from ..core import speech
        speech.speak(self.api.cosmo, text)

    def speak_random(self, text_list):
        self.speak(random.choice(text_list))

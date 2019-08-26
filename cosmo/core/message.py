# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

from . import handler

def search(cosmo,msg):
    intents = []
    for skill in cosmo.skills:
        for intent in skill.intents:
            intents.append(intent)

    print(handler.find_intent(intents, msg.query))


class Message:
    def __init__(self, query):
        self.query = query

        self.result = None
        self.arguments = {}

    def search(self, cosmo):
        return search(cosmo, self)

    def execute(self):
        pass


from . import handler


def search(cosmo, msg):
    intents = []
    for skill in cosmo.skills:
        for intent in skill.intents:
            intents.append(intent)

    return handler.find_intent(intents, msg.query)


class Message:
    def __init__(self, query):
        self.query = query

        self.result = None
        self.arguments = {}

    def search(self, cosmo):
        valid, intent, score, args = search(cosmo, self)
        self.result = MessageResult(valid, intent, score, args)
        return valid

    def execute(self, cosmo):
        if self.result.valid:
            self.arguments = self.result.arguments
            self.result.intent.invoke(cosmo,self)


class MessageResult:
    def __init__(self, valid, intent, score, args):
        self.valid = valid
        self.intent = intent
        self.score = score
        self.arguments = args

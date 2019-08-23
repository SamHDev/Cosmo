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

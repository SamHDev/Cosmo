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

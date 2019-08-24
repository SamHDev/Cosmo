# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

class TriggerRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

        self.listening = False

    def listen(self):
        self.listening = True

class SpeechRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

    def listen(self):
        pass
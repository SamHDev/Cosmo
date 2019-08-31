
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
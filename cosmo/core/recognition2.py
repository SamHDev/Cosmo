

class CosmoTriggerRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

        self.listening = False

    def listen(self):
        self.cosmo.chrome.socket.send("cmd.listen")
        self.listening = True

class CosmoSpeechRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

    def listen(self):
        pass
class CosmoRecognition:
    def __init__(self, cosmo):
        self.cosmo = cosmo
        self.callbacks = []

    def invoke(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def callback(self, func):
        self.callbacks.append(func)


class CosmoTriggerRecognition(CosmoRecognition):
    def __init__(self, cosmo):
        CosmoRecognition.__init__(self,cosmo)

        self.listening = False
        self.callbacks = []
        self.cmd = None

    def listen(self):
        self.cmd = input("CMD> ")
        self.invoke()


class CosmoSpeechRecognition(CosmoRecognition):
    def __init__(self, cosmo):
        CosmoRecognition.__init__(self,cosmo)

    def listen(self):
        self.invoke(self.cosmo.trigger_rec.cmd)

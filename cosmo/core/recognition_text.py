class Recognition:
    def __init__(self, cosmo):
        self.cosmo = cosmo
        self.callbacks = []

    def invoke(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def callback(self, func):
        self.callbacks.append(func)


class TriggerRecognition(Recognition):
    def __init__(self, cosmo):
        Recognition.__init__(self, cosmo)

        self.listening = False
        self.callbacks = []
        self.cmd = None

    def listen(self):
        self.cmd = input("Input> ")
        self.invoke()


class SpeechRecognition(Recognition):
    def __init__(self, cosmo):
        Recognition.__init__(self, cosmo)

    def listen(self):
        self.invoke(self.cosmo.trigger_rec.cmd)

# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

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

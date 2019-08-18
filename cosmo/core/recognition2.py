# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

class TriggerRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

        self.listening = False

    def listen(self):
        self.cosmo.chrome.socket.send("cmd.listen")
        self.listening = True

class SpeechRecognition:
    def __init__(self,cosmo):
        self.cosmo = cosmo

    def listen(self):
        pass
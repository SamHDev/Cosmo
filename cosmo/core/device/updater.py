# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

# Version Updater will be here

class CosmoUpdater:
    def __init__(self, device):
        self.device = device
        self.cosmo = device.cosmo

    def request_update(self):
        pass
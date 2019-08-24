# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

import json
import requests

from .version import Version
from .api import DeviceAPI
from .wifi import *
from . import reset as cosmo_reset
from . import machine

# CosmoDevice Class This holds the device info from files, along side version checker and api for Cosmo. Kept it
# separate from the Main Cosmo (Session) Class because it's got nothing to do with the main Skill Running and
# Executing Function
class CosmoDevice:
    def __init__(self, cosmo):
        self.cosmo = cosmo

        # Create a Bunch of placeholder vars for the class to be later field on CosmoDevice.load()
        self.serial = None
        self.device_type = None
        self.device_manufacturer = None
        self.device_version = None

        self.name = None
        self.is_setup = None

        # Create our api vars
        self.update = Version(self)  # Version Check/Updater
        self.api = DeviceAPI(self)  # CosmoDeviceAPI

        self.wifi = Wifi(self)
        self.hotspot = WifiHotspot(self)

        self.reset = cosmo_reset
        self.machine = machine

    def load(self):
        # Load the device manifest. Kept put in file than hardcoded because saves time later down the road if
        # multiple devices are involved, that way we just use the same software
        file_device = json.load(open("data/device/core/device.json"))
        self.serial = file_device["id"]  # Serial Code
        self.device_type = file_device["device"]["type"]  # Device Type e.g. CosmoHome
        self.device_manufacturer = file_device["device"]["manufacturer"]  # Device Manufacturer (Us silly billy)
        self.device_version = file_device["device"]["version"]  # Device Hardware Version. Not needed, nice to have.

        # Get Name Data
        file_data = json.load(open("data/device/data.json"))
        self.name = file_data["name"]
        self.is_setup = file_data["setup"]

        self.update.load()  # Load Update Files for Version Check/Updater API
        self.hotspot.load()
        self.wifi.load()

    def prepare(self):
        self.api.prepare()  # Prepare Web API

        # self.start_wifi()  # Start Wifi Call (to be called from main (session) class

        # Check if we have a modem
        if self.wifi.modem is None:
            self.wifi.modem = self.wifi.find_modem()
            self.wifi.save()
            if self.wifi.modem is None:
                self.wifi.logger.error("Invalid Wifi Interface. Failed to find one")
        if self.hotspot.modem is None:
            self.hotspot.modem = self.wifi.find_modem()

    def start_wifi(self):
        # Wifi Management
        if self.wifi.status()[0]:
            self.wifi.disconnect()  # Force Disconnect to stop errors.
        if self.wifi.configured():
            #self.wifi.connect()
            self.hotspot.start()
        else:
            self.hotspot.start()

    def start(self):
        # Just Testing. to be called from Cosmo Main (Session) Class
        # self.update.refresh_key()
        #self.update.check_update()  # Check Update Version

        self.api.start_threaded()  # Start API Server

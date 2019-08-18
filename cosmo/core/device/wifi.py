# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import wireless
import wifi
import json
import subprocess
import re
import platform
import atexit
from ...api.logger import CosmoSkillLogger

nmcli = "nmcli"


# Cosmo Wifi Class - For Connecting to Wifi Networks and Reading Wifi Config
class CosmoWifi:
    def __init__(self, device):
        self.device = device

        # Create our vars
        self.wifi_ssid = None
        self.wifi_password = None
        self.modem = None

        # Custom Logger time from that lengthy import above
        self.logger = CosmoSkillLogger("WifiManager")

        self._register_exit_handler()

    # Check if we can run nmcli on linux
    @staticmethod
    def check_platform():
        if platform.system() == "Linux":
            out = subprocess.check_call("nmcli -v", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return out == 0
        else:
            return False

    # Get Data From File
    def load(self):
        data = json.load(open("data/device/wifi.json"))
        self.wifi_ssid = data["wifi"]["ssid"]
        self.wifi_password = data["wifi"]["password"]
        self.modem = data["modem"]

    # Check the status of the modem
    def status(self):
        if not self.check_platform():
            self.logger.warn("Failed to Execute 'Status Check' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Checking Status of interface '{self.modem}'")
        try:
            out = subprocess.check_output(f"{nmcli} d show {self.modem}", shell=True).decode("UTF-8")
        except subprocess.CalledProcessError:
            return False, None
        data = re.compile(r"GENERAL\.STATE:[ ]*([0-9]*) ([\(\)a-z]*)").findall(out)
        data = data[0][1].replace("(", "").replace(")", "")
        return data == "connected", data

    def connect(self):
        if not self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Connection' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Connecting to '{self.wifi_ssid}' on interface'{self.modem}'")
        if not self.configured(): return None
        cmd = f"{nmcli} d wifi connect \"{self.wifi_ssid}\" password \"{self.wifi_password}\" ifname \"{self.modem}\""
        try:
            out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        except subprocess.CalledProcessError:
            return False
        self.logger.debug(f"Connected to '{self.wifi_ssid}'")
        return "successfully" in out

    def configured(self):
        return None not in [self.wifi_ssid, self.wifi_password]

    def disconnect(self):
        if not self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Disconnection' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Disconnecting from '{self.wifi_ssid}' on interface {self.modem}")
        cmd = f"{nmcli} d disconnect \"{self.modem}\""
        try:
            out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        except subprocess.CalledProcessError:
            return False
        return "successfully" in out

    def save(self):
        with open("data/device/wifi.json", "r") as f:
            data = json.loads(f.read())
        data["wifi"]["ssid"] = self.wifi_ssid
        data["wifi"]["password"] = self.wifi_password
        data["modem"] = self.modem
        with open("data/device/wifi.json", "w") as f:
            f.write(json.dumps(data))

    def find_modem(self):
        try:
            data = re.compile(r"([a-zA-Z0-9]+) *wifi").findall(subprocess.check_output(f"{nmcli} d", shell=True).decode("UTF-8"))
            return data[0]
        except IndexError:
            return None
        except subprocess.SubprocessError:
            return None

    def _register_exit_handler(self):
        @atexit.register
        def _exit_handler():
            if self.status()[0]:
                self.logger.warn("Stopping Wifi Connection, as was not closed before code exit. ")
                self.disconnect()


class CosmoWifiHotspot:
    def __init__(self, device):
        self.device = device
        self.ssid = None

        self.modem = None
        self.con_name = "cosmo_host"

        # Custom Logger time from that lengthy import above
        self.logger = CosmoSkillLogger("WifiHotspot")

        self._register_exit_handler()

    def status(self):
        return CosmoWifi.status(self) # Works, Trust me.

    def load(self):
        if self.ssid is None:
            ssid_number = str(int(self.device.serial.split("-", 1)[0], 16) / 10000).split(".", 1)[1]
            self.ssid = self.device.device_type + "-" + ssid_number
        data = json.load(open("data/device/wifi.json"))
        self.modem = data["modem"]

    def start(self):
        self.logger.debug(f"Starting Hotspot on '{self.modem}'")
        if not self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Hotspot Start' due to platform compatibility Issues.")
            return None
        cmd = f"{nmcli} d wifi hotspot ifname \"{self.modem}\" con-name \"{self.con_name}\" ssid \"{self.ssid}\""
        try:
            out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        except subprocess.CalledProcessError:
            return False
        self.logger.debug(f"Created Hotspot '{self.ssid}' on {self.modem}")
        return "successfully" in out

    def stop(self):
        if not self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Hotspot Stop' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Stopping hotspot '{self.ssid}' on interface {self.modem}")
        cmd = f"{nmcli} d disconnect \"{self.modem}\""
        try:
            out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        except subprocess.CalledProcessError:
            return False
        return "successfully" in out

    def _register_exit_handler(self):
        @atexit.register
        def _exit_handler():
            if self.status()[0]:
                self.logger.warn("Stopping Hotspot Connection, as was not closed before code exit. ")
                self.stop()

    def check_platform(self):
        return CosmoWifi.check_platform()

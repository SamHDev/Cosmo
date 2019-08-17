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
        if self.check_platform():
            self.logger.warn("Failed to Execute 'Status Check' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Checking Status of interface '{self.modem}'")
        out = subprocess.check_output(f"{nmcli} d show {self.modem}", shell=True).decode("UTF-8")
        data = re.compile(r"GENERAL\.STATE:[ ]*([0-9]*) ([\(\)a-z]*)").findall(out)
        data = data[0][1].replace("(", "").replace(")", "")
        return data == "connected", data

    def connect(self):
        if self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Connection' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Connecting to '{self.wifi_ssid}' on interface'{self.modem}'")
        if not self.configured(): return None
        cmd = f"{nmcli} d wifi connect \"{self.wifi_ssid}\" password \"{self.wifi_password}\" ifname \"{self.modem}\""
        out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        self.logger.debug(f"Connected to '{self.wifi_ssid}'")
        return "successfully" in out

    def configured(self):
        return None not in [self.wifi_ssid, self.wifi_password]

    def disconnect(self):
        if self.check_platform():
            self.logger.warn("Failed to Execute 'WIFI Disconnection' due to platform compatibility Issues.")
            return None
        self.logger.debug(f"Disconnecting from '{self.wifi_ssid}' on interface {self.modem}")
        cmd = f"{nmcli} d disconnect \"{self.modem}\""
        out = subprocess.check_output(cmd, shell=True).decode("UTF-8")
        return "successfully" in out

    def save(self):
        with open("data/device/wifi.json", "w") as f:
            f.write("close")


class CosmoWifiHotspot:
    def __init__(self, device):
        self.device = device
        self.ssid = None

    def load(self):
        if self.ssid is None:
            ssid_number = str(int(self.device.serial.split("-", 1)[0], 16) / 10000).split(".", 1)[1]
            self.ssid = self.device.device_type + "-" + ssid_number

    def start(self):
        self.load

    def stop(self):
        pass

import wireless
import json

class CosmoWifi:
    def __init__(self, device):
        self.device = device

        self.wifi_ssid = None
        self.wifi_password = None

        self.wifi = wireless.Wireless()

    def load(self):
        data = json.loads(open("data/device/wifi.json"))

    def connect(self):
        wireless.Wireless


class CosmoWifiHotspot:
    def __init__(self, device):
        self.device = device
        self.ssid = None
        self.ap = None

    def load(self):
        if self.ssid is None:
            ssid_number = str(int(self.device.serial.split("-", 1)[0], 16)/10000).split(".",1)[1]
            self.ssid = self.device.device_type + "-" + ssid_number
            print(self.ssid)

    def start(self):
        pass

    def stop(self):
        pass

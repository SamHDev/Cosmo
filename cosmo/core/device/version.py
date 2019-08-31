

import json
import requests


# Get Version Int
def get_version_int(name):
    return int(name.replace(".", ""))


# Cosmo Version Main Class
class Version:
    def __init__(self, device):
        self.device = device
        self.version_number = None
        self.version_id = None
        self.version_hash = None
        self.version_date = None

    def load(self):
        # Load Data from Update File.
        file_update = json.load(open("data/device/core/update.json"))
        self.version_number = file_update["version_number"]
        self.version_id = file_update["version_id"]
        self.version_hash = file_update["version_hash"]
        self.version_date = file_update["version_date"]

    def refresh_key(self):
        # Refresh API Updater KEY
        # You probably understand this shit, no commenting needed.
        self.device.cosmo.logger.debug("Connecting to Updater Service to request fresh update key")
        try:
            r = requests.post("https://api.cosmosmarthome.com/updater/newkey",
                              data={"serial": self.device.serial, "key": self.version_hash})
            data = r.json()
            # print(data)
            if not data["status"]["success"]:
                self.device.cosmo.logger.error("Failed to connect to Updater Service: " + data["data"]["error"])
            else:
                self.device.cosmo.logger.debug("Successfully Received New Update Hash from Server")
                file_update = json.load(open("data/device/core/update.json"))
                file_update["version_hash"] = data["data"]["new_hash"]
                with open("data/device/update.json", "w") as f:
                    f.write(json.dumps(file_update))

        except:
            self.device.cosmo.logger.error("Failed to communicate to Updater Service")

    def check_update(self):
        # Check API Version
        # You probably understand this shit, no commenting needed.
        self.device.cosmo.logger.debug("Connecting to Updater Service to request latest version details")
        try:
            r = requests.post("https://api.cosmosmarthome.com/updater/check",
                              data={"serial": self.device.serial, "key": self.version_hash})
            # print(r.text)
            data = r.json()
            # print(data)
            if not data["status"]["success"]:
                self.device.cosmo.logger.warn("Failed to communicate to Updater Service: " + data["data"]["error"])
                return None
            else:
                self.device.cosmo.logger.debug(
                    f"Found Latest Version as '{data['data']['update_version']}' vs '{self.version_number}' "
                    f"({get_version_int(data['data']['update_version'])}:{get_version_int(self.version_number)})")

                if get_version_int(data['data']['update_version']) > get_version_int(self.version_number):
                    return True
                else:
                    return False

        except:
            import traceback
            traceback.print_exc()
            self.device.cosmo.logger.error("Failed to connect to Updater Service")
            return None

    def update(self):
        # Updater shit here
        pass

# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart, SamHDev, https://github.com/samhdev


from ..web import *
import json
import uuid
import time


def register(self):
    @self.web.route("/setup/check")
    def setup_check():
        return api_response(200, data={
            "setup": self.device.is_setup
        })

    @self.web.route("/setup/request")
    def setup_request():
        if not self.device.is_setup:
            if len(self.setup_tokens) != 0:
                return api_error(409, "Setup Locked. Currently In Use")
            else:
                new_token = str(uuid.uuid4())
                self.setup_tokens.append(new_token)
                return api_response(data={"token": new_token})
        else:
            return api_error(403, "Setup Locked. Device already setup")

    # Device Name Setup Value Writer
    @self.web.route("/setup/device_name", methods=["GET"])
    def setup_value_get_device_name():
        if not ((not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens):
            return api_error(403, "Requires Setup Token")
        return api_response(data={"device_value": self.device.name})

    @self.web.route("/setup/device_name", methods=["POST"])
    def setup_value_set_device_name():
        if not ((not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens):
            return api_error(403, "Requires Setup Token")
        device_name = flask.request.form.get("value", default=None)
        if device_name == None:
            return api_error(400, "Invalid Value")
        if len(device_name) < 4:
            return api_error(400, "Invalid Value, Must be larger than 4 characters")
        if len(device_name) > 32:
            return api_error(400, "Invalid Value, Must be smaller than 32 characters")
        file_data = json.load(open("data/device/data.json"))
        file_data["name"] = device_name
        with open("data/device/data.json", "w") as f:
            f.write(json.dumps(file_data))
        self.device.load()
        return api_response(data={"device_name": self.device.name})

    # Device Name Setup Value Writer
    @self.web.route("/setup/wifi", methods=["GET"])
    def setup_value_get_wifi():
        if not ((not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens):
            return api_error(403, "Requires Setup Token")
        return api_response(
            data={"ssid": self.device.wifi.wifi_ssid, "password": "*" * len(self.device.wifi.wifi_password),
                  "configured": self.device.wifi.configured(), "status": list(self.device.wifi.status())})

    @self.web.route("/setup/wifi", methods=["POST"])
    def setup_value_set_wifi():
        if not ((not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens):
            return api_error(403, "Requires Setup Token")
        ssid = flask.request.form.get("ssid", default=None)
        password = flask.request.form.get("password", default=None)
        if ssid == None or password == None:
            return api_error(400, "Invalid Value")

        self.device.wifi.wifi_ssid = ssid
        self.device.wifi.wifi_password = password
        self.device.wifi.save()
        return api_response(
            data={"ssid": self.device.wifi.wifi_ssid, "password": "*" * len(self.device.wifi.wifi_password)})

    @self.web.route("/setup/wifi", methods=["PUT"])
    def setup_value_command_wifi():
        if not ((not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens):
            return api_error(403, "Requires Setup Token")
        if not self.device.wifi.configured():
            return api_error(400, "Requires Wifi Details to be submitted")
        if self.device.hotspot.status()[0]:
            self.device.hotspot.stop()
        if self.device.wifi.status()[0]:
            self.device.wifi.disconnect()
        success = self.device.wifi.connect()
        time.sleep(1)
        if success == True:
            return api_response(data={"msg": "Attempting Connection"})
        else:
            return api_response(data={"msg": "Connection Failed"})





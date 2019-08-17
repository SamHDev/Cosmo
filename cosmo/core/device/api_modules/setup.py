from ..web import *
import json

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
    @self.web.route("/setup/value/device_name", methods=["GET"])
    def setup_value_get_device_name():
        if (not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens:
            return api_response(data={"key": "device_name", "value": self.device.name})

    @self.web.route("/setup/value/device_name", methods=["POST"])
    def setup_value_set_device_name():
        if (not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens:
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
            return api_response(data={"key": "device_name", "value": self.device.name})

    # Device Name Setup Value Writer
    @self.web.route("/setup/value/wifi", methods=["GET"])
    def setup_value_get_wifi():
        if (not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens:
            return api_response(data={"key": "device_name", "value": {"ssid": self.device.wifi.ssid, "pass": None}})

    @self.web.route("/setup/value/wifi", methods=["POST"])
    def setup_value_set_wifi():
        if (not self.device.is_setup) and flask.request.args.get("token", default=None) in self.setup_tokens:
            ssid = flask.request.form.get("ssid", default=None)
            password = flask.request.form.get("password", default=None)
            if ssid == None or password == None:
                return api_error(400, "Invalid Value")

            with open("data/device/data.json", "w") as f:
                f.write(json.dumps(file_data))
            self.device.load()
            return api_response(data={"key": "device_name", "value": self.device.name})

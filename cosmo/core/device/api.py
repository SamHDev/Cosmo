import flask
import threading
import json
import time
import uuid


def api_response(code=200, success=None, status_msg=None, data=None):
    if success is None:
        success = (code == 200)
    if status_msg is None:
        status_msg = {200: "Request Successful", 400: "Bad Request", 403: "Forbidden", 500: "Server Error",
                      503: "Server/Service/Endpoint Unavailable", 404: "Endpoint Not Found", 409: "Request Conflict",
                      418: "I'm a teapot"}[code]

    msg = {
        "status": {
            "code": code,
            "success": success,
            "msg": status_msg
        },
        "data": data
    }

    return flask.Response(json.dumps(msg), status=code, mimetype="application/json")


def json_response(data, code=200):
    return flask.Response(json.dumps(data), status=code, mimetype="application/json")


def api_error(code, error_msg):
    return api_response(code, False, data={"error": error_msg})


class CosmoDeviceAPI:
    def __init__(self, device):
        self.device = device
        self.cosmo = device.cosmo
        self.web = flask.Flask(__name__)
        self.api_version = "1.0"

        self.setup_tokens = []

    def start(self):
        self.web.run("0.0.0.0", 12890)

    def start_threaded(self):
        thd = threading.Thread(target=self.start, daemon=True)
        thd.start()
        return thd

    def prepare(self):
        @self.web.errorhandler(404)
        def resource_not_found(e):
            return api_error(404, str(e))

        @self.web.route("/")
        def hello_world():
            return f"CosmoAPI/{self.api_version}"

        @self.web.route("/ping")
        def ping():
            return api_response(200, data={"msg": "Pong", "server_time": time.time()})

        @self.web.route("/info/device")
        def info_device():
            return api_response(200, data={
                "name": self.cosmo.device.name,
                "serial": self.cosmo.device.serial,
                "device": {
                    "type": self.cosmo.device.device_type,
                    "manufacturer": self.cosmo.device.device_manufacturer,
                    "version": self.cosmo.device.device_version
                }
            })

        @self.web.route("/info/hardware")
        def info_hardware():
            import platform
            return api_response(200, data={
                "serial": self.cosmo.device.serial,
                "platform": platform.platform(),
                "processor": platform.processor(),
                "system": platform.system()
            })

        @self.web.route("/info/version")
        def info_version():
            return api_response(200, data={
                "serial": self.cosmo.device.serial,
                "version": self.device.update.version_number
            })

        @self.web.route("/info/address")
        def info_address():
            import socket
            import requests
            import uuid
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            mac = hex(uuid.getnode())[2:]
            mac = f"{mac[0:2]}:{mac[2:4]}:{mac[4:6]}:{mac[6:8]}:{mac[8:10]}:{mac[10:12]}"
            return api_response(200, data={
                "hostname": host_name,
                "ip": {
                    "local": host_ip,
                    "public": requests.get("https://api.ipify.org").text
                },
                "mac": mac
            })

        @self.web.route("/info")
        def info_info():
            import socket
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            return api_response(200, data={
                "name": self.cosmo.device.name,
                "ip": host_ip,
                "serial": self.cosmo.device.serial,
                "setup": self.device.is_setup
            })

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

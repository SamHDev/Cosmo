# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

from ..web import *
import json

def register(self):
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
# Sam's Base Device API
# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart, SamHDev, https://github.com/samhdev
# Note: Please ask permission from 'SamHDev' before modifying this file

import flask
import threading
import json
import time
import uuid

# Import Web APi shit
from .web import *
from .api_modules import info,setup


class DeviceAPI(WebServer):
    def __init__(self, device):
        WebServer.__init__(self, device)

        self.api_version = "1.0"
        self.setup_tokens = []

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


        # Import Modules
        info.register(self)
        setup.register(self)


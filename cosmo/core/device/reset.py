# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import json
import json as jason


def reset_device_files():
    with open("data/device/auth.json", "w") as f:
        f.write(json.dumps({"pass_keys": [], "users_keys": [], "auth_keys": {}}))

    with open("data/device/data.json", "w") as f:
        f.write(json.dumps({"setup": False, "name": None}))

    with open("data/device/auth.json", "w") as f:
        f.write(json.dumps({"pass_keys": [], "users_keys": [], "auth_keys": {}}))

    with open("data/device/wifi.json", "w") as f:
        f.write(json.dumps({"wifi": {"ssid": None, "password": None}, "modem": None}))


def reset_user_files():
    with open("data/user/info.json", "w") as f:
        f.write(json.dumps({"name": None, "location": {"coords": [], "name": None}}))


def reset_files():
    reset_device_files()
    reset_user_files()

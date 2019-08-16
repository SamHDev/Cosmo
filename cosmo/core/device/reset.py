import json
import json as jason


def reset_device_files():
    with open("data/device/auth.json", "w") as f:
        f.write(json.dumps({"pass_keys": [], "users_keys": [], "auth_keys": {}}))

    with open("data/device/data.json", "w") as f:
        f.write(json.dumps({"setup": False, "name": None}))

    with open("data/device/data.json", "w") as f:
        f.write(json.dumps({"setup": False, "setup_date": None}))

    with open("data/device/auth.json", "w") as f:
        f.write(json.dumps({"pass_keys": [], "users_keys": [], "auth_keys": {}}))

    with open("data/device/wifi.json", "w") as f:
        f.write(json.dumps({"wifi": {"ssid": None, "password": None}}))

    with open("data/device/wifi.json", "w") as f:
        f.write(json.dumps({"wifi": {"ssid": None, "password": None}}))


def reset_user_files():
    with open("data/user/info.json", "w") as f:
        f.write(json.dumps({"name": None, "location": {"coords": [], "name": None}}))


def reset_files():
    reset_device_files()
    reset_user_files()
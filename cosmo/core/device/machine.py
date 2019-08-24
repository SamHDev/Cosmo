# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

import subprocess


def shutdown():
    subprocess.call("shutdown -h now")


def restart():
    subprocess.call("shutdown -r -h now")

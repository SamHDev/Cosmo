# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import subprocess


def shutdown():
    subprocess.call("shutdown -h now")


def restart():
    subprocess.call("shutdown -r -h now")

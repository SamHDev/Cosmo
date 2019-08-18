# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.

import sys
import datetime


# Better Logger than Glebs Logger. Move to New File and formatted nicely. Take that gleb.

logger_colors = dict(reset="\u001b[0m", white="\u001b[37m", black="\u001b[30m", red="\u001b[31m", green="\u001b[32m",
                     yellow="\u001b[33m", blue="\u001b[34m", purple="\u001b[35m", cyan="\u001b[36m")

def _log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


class Logger:
    def __init__(self, debug=False, app_name=None):
        self.print_debug = debug
        self.app_name = app_name

    def _format(self, ltype, msg, app_name=None, color=None):
        if app_name is None:
            if self.app_name is None:
                app_name = "Cosmo"
            else:
                app_name = self.app_name

        f_time = datetime.datetime.utcnow().strftime("%H:%M:%S")
        color_pre = ""
        color_suf = ""
        if color is not None:
            if color in logger_colors.keys():
                color_pre = logger_colors[color]
            else:
                color_pre = color
            color_suf = logger_colors["reset"]
        return "{app}> {color_pre} {time} [{type}] {msg}{color_suf}".format(app=app_name, time=f_time, type=ltype, msg=msg, color_pre=color_pre, color_suf=color_suf)

    def log(self, log_type, log_msg, app_name=None, color=None):
        _log(self._format(log_type, log_msg, app_name=app_name, color=color))

    def info(self, msg):
        self.log("INFO", msg, color="cyan")

    def ok(self, msg):
        self.log("-OK-", msg, color="green")

    def warn(self, msg):
        self.log("WARN", msg, color="yellow")

    def error(self, msg):
        self.log("ERRR", msg, color="red")

    def debug(self, msg):
        if self.print_debug:
            self.log("DBUG", msg)

    def sep(self):
        print("-" * 70)

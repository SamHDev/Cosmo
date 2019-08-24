import sys
import datetime

# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Logger Config Handler
logger_default_appname = "Cosmo"
logger_config = {"format": 0, "debug": True, "colour": True}
import json

try:
    logger_config = json.load(open("data/config/logger.json"))
except:
    pass  # Something Went Wrong, Oh well, default it is then.

logger_colours = dict(reset="\u001b[0m", white="\u001b[37m", black="\u001b[30m", red="\u001b[31m", green="\u001b[32m",
                     yellow="\u001b[33m", blue="\u001b[34m", purple="\u001b[35m", cyan="\u001b[36m")

logger_styles = [
    {
        "root": "{app}> {colour_pre} {time} [{type}] {msg}{colour_suf}",
        "info": "INFO",
        "ok": "-OK-",
        "warn": "WARN",
        "error": "ERRR",
        "fatal": "FATAL",
        "debug": "Debug",
        "separator": "-"*70
    },
    {
        "root": "{colour_pre} {time}/{app} {type} {msg}{colour_suf}",
        "info": "   ",
        "ok": "-- ",
        "warn": "!  ",
        "error": "!! ",
        "fatal": "!!!",
        "debug": ">  ",
        "separator": "-"*70
    }
]


def _log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


class Logger:
    def __init__(self, debug=None, app_name=None, config=logger_config):
        self.print_debug = debug
        self.app_name = app_name
        self.config = config

        if self.print_debug is None:
            self.print_debug = self.config["debug"]

    def _format(self, ltype, msg, app_name=None, colour=None):
        if app_name is None:
            if self.app_name is None:
                app_name = logger_default_appname
            else:
                app_name = self.app_name
        if ltype in logger_styles[self.config["style"]].keys():
            ltype = logger_styles[self.config["style"]][ltype]

        f_time = datetime.datetime.utcnow().strftime("%H:%M:%S")
        colour_pre = ""
        colour_suf = ""
        if not self.config["colour"]:
            colour = None
        if colour is not None:
            if colour in logger_colours.keys():
                colour_pre = logger_colours[colour]
            else:
                colour_pre = colour
            colour_suf = logger_colours["reset"]
        return logger_styles[self.config["style"]]["root"].format(app=app_name, time=f_time, type=ltype,
                                                                            msg=msg, colour_pre=colour_pre,
                                                                            colour_suf=colour_suf)

    def log(self, log_type, log_msg, app_name=None, colour=None):
        _log(self._format(log_type, log_msg, app_name=app_name, colour=colour))

    def __call__(self, msg):
        return self.debug(msg)

    def info(self, msg):
        self.log("info", msg, colour="cyan")

    def ok(self, msg):
        self.log("ok", msg, colour="green")

    def warn(self, msg):
        self.log("warn", msg, colour="yellow")

    def error(self, msg):
        self.log("error", msg, colour="red")

    def fatal(self, msg):
        self.log("fatal", msg, colour="purple")

    def debug(self, msg):
        if self.print_debug:
            self.log("debug", msg)

    def sep(self):
        self.separator()

    def separator(self):
        _log(logger_styles[self.config["style"]]["separator"])

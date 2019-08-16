import sys
import datetime

# Cosmo Skill Logger (No shit sherlock)
# Because the importing the core was causing errors and I a lazy asshole so. bite me cunts.

class CosmoSkillLogger:
    def __init__(self, app_name, debug=False):
        self.print_debug = debug
        self.app_name = app_name

    def setdebug(self, value):
        self.print_debug = value

    def _log(self, text):
        sys.stdout.write(text + "\n")
        sys.stdout.flush()

    def _format(self, ltype, msg, app_name=None):
        if app_name is None:
            if self.app_name is None:
                app_name = "Cosmo"
            else:
                app_name = self.app_name

        f_time = datetime.datetime.utcnow().strftime("%H:%M:%S")
        return "{app}> {time} [{type}] {msg}".format(app=app_name, time=f_time, type=ltype, msg=msg)

    def log(self, log_type, log_msg, app_name=None):
        self._log(self._format(log_type, log_msg, app_name=app_name))

    def info(self, msg):
        self.log("INFO", msg)

    def ok(self, msg):
        self.log("-OK-", msg)

    def warn(self, msg):
        self.log("WARN", msg)

    def error(self, msg):
        self.log("ERRR", msg)

    def debug(self, msg):
        if self.print_debug:
            self.log("DBUG", msg)

from .logger import CosmoLogger
from .skills import find_skills, load_skills
from .message import find_intent, execute_intent
# from .recognition import * #Demo Voice Rec
from .recognition_text import *  # Demo Text Input
import time

from .device import CosmoDevice


# Cosmo Main Class (Session) (Quick Fix from Gleb's Code Removal. Fuck you gleb)
class Cosmo:
    def __init__(self):
        # Create Logger
        self.logger = CosmoLogger(debug=True)

        # Create Empty Lists for Skills to load
        self.modules = []
        self.skills = []

        # Create Recognition Objects
        self.trigger_rec = CosmoTriggerRecognition(self)
        self.command_rec = CosmoSpeechRecognition(self)

        self.device = CosmoDevice(self)

        self.contexts = {}

    # Prepare Function (For Preloading shit)
    def prepare(self):
        self.logger.sep()
        self.device.load()
        # self.device.update.check_update()

        skills = find_skills(self)
        load_skills(self, skills)

        self.device.prepare()

        if self.device.update.check_update():
            pass

        print(self.device.wifi.find_modem())

    # Start Function (Starts the reset of the uttlery shite code)
    def start(self):
        self.logger.sep()
        self.logger.info(
            f"Starting {self.device.device_type}/{self.device.device_version} running {self.device.update.version_number}")

        self.logger.ok("Starting Network Wifi")
        self.device.start_wifi()

        self.logger.ok("Starting Cosmo Main Threads")

        self.device.start()

        # Create Callbacks for Recognition Objects (Quick Fix)
        @self.trigger_rec.callback
        def callback():
            self.command_rec.listen()

        @self.command_rec.callback
        def callback2(cmd):
            intent = find_intent(self, cmd)
            if intent is not None:
                execute_intent(self, intent)
            else:
                print("FAILED")
            time.sleep(1)
            self.trigger_rec.listen()

        self.logger.sep()
        # Listen Bitch
        self.trigger_rec.listen()

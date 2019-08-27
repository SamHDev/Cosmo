from cosmo.logger import Logger, SubLogger
from .skills import find_skills, load_skills
from .message import Message
# from .recognition import * #Demo Voice Rec
from .recognition_text import *  # Demo Text Input
import time

from .device import CosmoDevice


# Cosmo Main Class (Session)
class Cosmo:
    def __init__(self):
        # Create Logger
        self.logger = Logger(debug=True)

        # Create Empty Lists for Skills to load
        self.modules = []
        self.skills = []

        # Create Recognition Objects
        self.trigger_rec = TriggerRecognition(self)
        self.command_rec = SpeechRecognition(self)

        self.device = CosmoDevice(self)

        self.contexts = {}

    # Prepare Function (For Preloading shit)
    def prepare(self):
        self.logger.sep()
        self.device.load()
        # self.device.update.check_update()

        skills = find_skills(self)
        load_skills(self, skills)  # Comment/Uncomment this to enable/disable skill loading

        self.device.prepare()

        if self.device.update.check_update():
            pass

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
            msg = Message(cmd)
            if msg.search(self):
                msg.execute(self)
            else:
                print("Failed")
            time.sleep(1)
            self.trigger_rec.listen()

        self.logger.sep()
        # Listen Bitch
        self.trigger_rec.listen()

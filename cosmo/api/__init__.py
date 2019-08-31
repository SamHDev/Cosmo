from . import skill
from . import intent
from . import actions
from . import fs
from cosmo import logger
from . import contexts
from . import argtypes
from .argtypes import IntentArgumentType, IntentArgumentTypeFromRegex
#from . import utils # wat for?



# API Wrapper (New API System)
class API:
    def __init__(self,debug=False):
        # Prepare Class types and Vars
        self.cosmo = None
        self.Skill = skill.Skill
        self.Intent = intent.Intent
        self.IntentHandler = intent.getIntentHandler(self)  # New Decorator for Glebs Intent System
        self.IntentArgumentType, self.IntentArgumentTypeFromRegex = IntentArgumentType, IntentArgumentTypeFromRegex

        self.skills_buffer = []

        # Load Manifest and find module path.
        self.path, self.root = fs.get_path()
        self.name, self.authors, self.version = fs.get_manifest(self)
        self.module = fs.get_invoking_module(2)

        # Load phrases and speech
        self.phrases = fs.get_phrases(self, "en")
        self.speech = fs.get_speech(self, "en")

        # Make Sub-Logger
        self.logger = logger.SubLogger(self.name,debug=debug)

        # Make classes for api to use
        self.fs = fs.FileAPI(self)  # FileSystem API
        self.context = contexts.Contexts(self)  # Context API

        self.ArgumentType = argtypes.ArgumentType
        self.IntentArgumentType = argtypes.IntentArgumentType
        self.IntentArgumentTypeRegex = argtypes.IntentArgumentTypeFromRegex

        self.api_skill = skill.Skill(self)  # Global Skill for Gleb's Awsome Register System

    def _set_cosmo(self, cosmo):
        # Cosmo Function Write
        self.cosmo = cosmo
        self.logger = cosmo.logger
        self.actions = actions.Actions(self)

        # self.find_skills() #Just an Idea Call

        # Apply skills from buffer into Cosmo
        if len(self.api_skill.intents) != 0:
            self.cosmo.skills.append(self.api_skill)
        for skillb in self.skills_buffer:
            skill_inst = skillb(self)
            skill_inst.setup()
            self.cosmo.skills.append(skill_inst)  # Create Skill Instance
            i = 0
            for skill_intent in skill_inst.intents:
                if type(skill_intent) == type:
                    skill_inst.intents[i] = skill_intent(self)
                    skill_inst.intents[i].setup()
                else:
                    skill_inst.intents[i] = skill_intent
                    skill_inst.intents[i].setup()
                i += 1


    def register_skill(self, skill: skill.Skill):
        # Write Skills to skill buffer
        self.skills_buffer.append(skill)

    # Just an Idea (Failed)
    def find_skills(self):
        for var in dir(self.module):
            if isinstance(getattr(self.module, var), skill.Skill):
                self.skills_buffer.append(getattr(self.module, var))

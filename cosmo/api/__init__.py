from . import skill
from . import intent
from . import actions
from . import fs
from cosmo import logger
from . import contexts

# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

# API Wrapper (New API System)
class API:
    def __init__(self):
        # Prepare Class types and Vars
        self.cosmo = None
        self.Skill = skill.Skill
        #self.Intent = intent.IntentClass(self) # I did this to allow intents to access the api.
        self.Intent = intent.Intent
        self.skills_buffer = []

        # Load Manifest and find module path.
        self.path, self.root = fs.get_path()
        self.name, self.authors, self.version = fs.get_manifest(self)
        self.module = fs.get_invoking_module(2)

        # Make Sub-Logger
        self.logger = logger.SkillLogger(self.name,debug=debug)

        # Load phrases
        self.phrases = fs.get_phrases(self, "en")

        # Make Sub-Logger
        self.logger = logger.SubLogger(self.name)

        # Make classes for api to use
        self.fs = fs.FileAPI(self)  # FileSystem API
        self.context = contexts.Contexts(self) # Context API

        # Prepare Class types and Vars
        self.cosmo = None
        self.Skill = skill.Skill
        self.Intent = intent.IntentClass(self) # I did this to allow intents to access the api.
        self.skills_buffer = []


    def _set_cosmo(self, cosmo):
        # Cosmo Function Write
        self.cosmo = cosmo
        self.logger = cosmo.logger
        self.actions = actions.Actions(self)


        # self.find_skills() #Just an Idea Call

        # Apply skills from buffer into Cosmo
        for skillb in self.skills_buffer:
            skill_inst = skillb(self)
            skill_inst.setup()
            self.cosmo.skills.append(skill_inst)  #Create Skill Instance
            i = 0
            for skill_intent in skill_inst.intents:
                skill_inst.intents[i] = skill_intent(self, skill_inst)
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
from . import skill
from . import intent
from . import actions
from . import fs
from . import logger
from . import contexts

# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

# API Wrapper (New API System)
class API:
    def __init__(self,debug=False):
        # Load Manifest and find module path.
        self.path, self.root = fs.get_path()
        self.name, self.authors, self.version = fs.get_manifest(self)
        self.module = fs.get_invoking_module(2)

        # Make Sub-Logger
        self.logger = logger.SkillLogger(self.name,debug=debug)

        # Load phrases
        self.phrases = fs.get_phrases(self, "en")

        # Make classes for api to use
        self.fs = fs.FileAPI(self)  # FileSystem API
        self.context = contexts.Contexts(self) # Context API

        # Prepare Class types and Vars
        self.cosmo = None
        self.Skill = skill.Skill
        self.Intent = intent.IntentClass(self) # I did this to allow intents to access the api.
        self.skills_buffer = []


    def _set_cosmo(self, cosmo):
        # Cosmo Function Write
        self.cosmo = cosmo
        self.logger = cosmo.logger
        self.actions = actions.Actions(self)


        # self.find_skills() #Just an Idea Call

        # Apply skills from buffer into Cosmo
        for skillb in self.skills_buffer:
            self.cosmo.skills.append(skillb)

    def register_skill(self, skill: skill.Skill):
        # Write Skills to skill buffer
        self.skills_buffer.append(skill)

    # Just an Idea (Failed)
    def find_skills(self):
        for var in dir(self.module):
            if isinstance(getattr(self.module, var), skill.Skill):
                self.skills_buffer.append(getattr(self.module, var))

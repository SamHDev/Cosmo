# Copyright (C) 2019 CosmoHome, LLC
# Unauthorized copying and usage of this file, via any medium is strictly prohibited
# Proprietary and confidential

from . import intent
from cosmo.logger import Logger
from functools import wraps


# Skill Wrapper
class Skill:
    def __init__(self, api):
        self.api = api
        self.intents = []
        self.find_intents()
        self.logger = Logger(app_name=self.__class__.__name__,debug=self.api.logger.print_debug)

    def setup(self):
        pass

    def register_intent(self, intent):
        intent.set_skill(self)
        self.intents.append(intent)

    # Just an Idea (Failed) VERY BIG FAILED
    def find_intents(self):
        for var in dir(self):
            if isinstance(getattr(self, var), intent.Intent):
                self.register_intent(getattr(self,var))

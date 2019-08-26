# Sam's Better epic Roblox CosmoHome Skill System suck my big fat juicy nipples the sequel: the return of hitler

#Not Finished

# GET API
import cosmo.api as cosmo

import datetime

api = cosmo.API()

file = api.fs.request_data_file("demo.txt")
if not file.exists():
    file.create()


class DemoSkill(api.Skill):
    def setup(self):
        self.register_intent(self.HelloIntent)
        
    class HelloIntent(api.IntentClass):
        def setup(self):
            self.add_raw_phrase("hello")
            self.add_callback(self.ex_callback)

        def ex_callback(self, e):
            api.actions.speak("Hello! I'm Cosmo")


api.register_skill(DemoSkill)

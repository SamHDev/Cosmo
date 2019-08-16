# Sam's Better epic Minecraft CosmoHome Skill System suck my nipples

# GET API
import cosmo.api as cosmo

# Other shitty imports stfu python
import datetime

# Create an API Object and Skill Cosmo
api = cosmo.API()
skill = api.Skill()
api.register_skill(skill)

# Create a file
file = api.fs.request_data_file_json("data.json")
file.exist_create()

api.logger.info("HELLO!")

# Create an Intent
hello_intent = api.Intent()
# Add A Phrase
hello_intent.add_phrase("Who Are You")


# Set a Callback
@hello_intent.callback
def hello_intent_callback(msg):
    api.actions.speak("Hi I'm Cosmo! The Smart AI Assistant!")


# Register to Skill
skill.register_intent(hello_intent)

help_intent = api.Intent()
help_intent.add_phrase("What do you do")


@help_intent.callback
def help_intent_callback(msg):
    api.actions.speak(
        "Glad You Asked! I Can Do Things Ranging From Telling You The Time All The Way To Ordering Food! All You Need "
        "To Do Is Just Ask!")


skill.register_intent(help_intent)

age_intent = api.Intent()
age_intent.add_phrase("How Old Are You")


@age_intent.callback
def age_intent_callback(msg):
    api.actions.speak_random(["Looking at my Internals I feel young!", "I'm born 2019"])


skill.register_intent(age_intent)

time_intent = api.Intent()
time_intent.add_phrase("What's The Time")


@time_intent.callback
def time_intent_callback(msg):
    time_output = datetime.datetime.now().strftime("%I : %M  %p")
    api.actions.speak(f"Right now is {time_output}")


skill.register_intent(time_intent)

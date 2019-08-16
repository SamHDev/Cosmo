# Skill API Docs

These are some quick docs on how to setup a skill with cosmo

### Setting up a skill

This is the basic structure of a skill:
 - Manifest (skill.json)
 - Main File (main.py)

##### Manifest
Example Manifest
```
{
  "name": "Demo Skill",
  "authors": ["SamHDev"],
  "version": 1,
  "update_url": null,
  "main": "skill.py"
}
 ```
 
 Manifest Values
 
| Key | Value Type | Example Value | Description |
| --- | --- | --- | --- |
| name | string | "Demo Skill" | The Skill Name for display |
| authors | list(string) | ["SamHDev"] | The Skill Authors for display |
| version | int | 1 | The version of the skill for update checking |
| update_url | string(url)(null) | https://cosmo.samh.dev/skills/demo.json | The file for update checking |
| main | string | "skill.py" | The Main python module to execute |


### Cosmo API (Method 1)

###### Import the Cosmo API
Get started by importing the required API Module.
```
import cosmo.api as cosmo
```
Next we can import the API Object.
```
api = cosmo.API()
```

###### Create a Skill
We can create a Skill Object to register intents
```
skill = api.Skill()
```
Then register the skill to the api
```
api.register_skill(skill)
```

###### Create an Intent
Create an Intent by using the API Object
```
demo_intent = api.Intent()
```
Add a trigger to the Intent with the phrase. You can add as many as you like
```
demo_intent.add_phrase("Who Are You")
```
Add a callback to the Intent as so:
```
@demo_intent.callback
def demo_intent_callback(msg):
   #Do Stuff Here
```

###### Using The API
The api allows us to access parts of cosmo. The most common usage is speaking.
We can do this by:
```
api.actions.speak("Hi I'm Cosmo! The Smart AI Assistant!")
```

### Cosmo API (Method 2)

###### Import the Cosmo API
Get started by importing the required API Module.
```
import cosmo.api as cosmo
```
Next we can create an API Object
```
api = cosmo.API()
```

###### Create a Skill
We can create a Subclass of the Skill Class
```
class DemoSkill(api.Skill):
    def setup(self):
        #CODE
```
The Create and then Register the Skill Object to the api
```
api.register_skill(DemoSkill())
```

###### Create an Intent
Create an Intent by using the API Object
```
    class HelloIntent(api.Intent):
        def setup(self):
            #CODE
```
Add a trigger to the Intent with the phrase. You can add as many as you like
```
demo_intent.add_phrase("Who Are You")
```
Add a callback to the Intent as so:
```
@demo_intent.callback
def demo_intent_callback(msg):
   #Do Stuff Here
```

###### Using The API
The api allows us to access parts of cosmo. The most common usage is speaking.
We can do this by:
```
api.actions.speak("Hi I'm Cosmo! The Smart AI Assistant!")
```


## API Reference (api)

### api.actions

##### .speak
The `api.actions.speak()` function uses Cosmo's TTS engine to output audio.
```
api.actions.speak("Hi I'm Cosmo! The Smart AI Assistant!")
```


##### .speak_random
The `api.actions.speak_random()` function takes in a random list of phrases to be spoken using `api.actions.speak()`
```
api.actions.speak_random(["Looking at my Internals I feel young!","I'm born 2019"])
```








import random

class SpeechNotFoundError(Exception):
    pass

# Demo Actions API
class Actions:
    def __init__(self, api):
        self.api = api
        
    def speak(self, speech, *format_list, **format_dict):
        if not speech in self.api.speech:
            raise SpeechNotFoundError(speech)
        else:
            self.speak_random(self.api.speech[speech],*format_list, **format_dict)
    def speak_raw(self, speech_text, *args, **kwargs):
        print(">> "+speech_text.format(*args, **kwargs))
        from ..core import speech
        speech.speak(self.api.cosmo, speech_text.format(*args, **kwargs))

    def speak_random(self, speech_text_list, *args, **kwargs):
        self.speak(random.choice(speech_text_list),*args, **kwargs)

import speech_recognition as sr
import pocketsphinx
from .handler import find_intent, execute_intent


class CosmoTriggerRecognition:
    def __init__(self, cosmo):
        self.cosmo = cosmo
        self.thd = None

        self.trigger = "cosmo"

    def listen(self):
        self.cosmo.logger.debug("Preparing Trigger Handler")
        from pocketsphinx import LiveSpeech
        speech = LiveSpeech(lm=False, keyphrase=self.trigger, kws_threshold=1e-20)
        self.cosmo.logger.debug("Listening for Trigger Word")
        for phrase in speech:
            print(phrase.segments(detailed=True))

            from pydub import AudioSegment
            from pydub.playback import play
            import os
            play(AudioSegment.from_file(os.path.abspath("cosmo/assets/sounds/activate.wav"), format="wav"))
            self.cosmo.logger.debug("Trigger Word Found")

            self.callback_func()

    def callback(self, func):
        self.callback_func = func


class CosmoSpeechRecognition:
    def __init__(self, cosmo):
        self.cosmo = cosmo
        self.thd = None

        self.trigger = "cosmo"

    def listen(self):
        rec = sr.Recognizer()
        self.cosmo.logger.debug("Listening for Command")
        with sr.Microphone() as mic:
            audio = rec.listen(mic)

        from pydub import AudioSegment
        from pydub.playback import play
        import os
        play(AudioSegment.from_file(os.path.abspath("cosmo/assets/sounds/deactivate.wav"), format="wav"))

        self.cosmo.logger.debug("Recognizing for Command")
        cmd = rec.recognize_google(audio)
        self.cosmo.logger.debug("Got Input: " + cmd)

        intent = find_intent(self.cosmo, cmd)
        execute_intent(self.cosmo, intent)

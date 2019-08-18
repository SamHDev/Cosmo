# Copyright (C) SamHDev, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Sam Huddart <sam02h.huddart@gmail.com>, August 2019
# Licensed to CosmoHome on a Temporary Basis. This may be revoked at any time.


from gtts import gTTS
import os
import uuid
import pydub
from pydub import playback
import playsound
import time
import playsound


# pydub.AudioSegment.ffmpeg = "C:/Program Files/ffmpeg/bin/"


# Speech Class (Demo) (Very Bad)

def speak(cosmo, msg):
    # Create File to save audio at
    file = "cache/voice/" + str(uuid.uuid4()) + "$$$.mp3"

    # Create Text Text to Speech
    tts = gTTS(text=msg, lang='en')
    tts.save(file.replace("$$$", "0"))

    # Load in pydub
    sound = pydub.AudioSegment.from_file(os.path.abspath(file.replace("$$$", "0")), format="mp3")
    octaves = 0.085

    # Pitch Shift
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
    pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})

    # Filter Shift
    filter_sound = pitch_sound.low_pass_filter(8000)
    # Save
    filter_sound.export(os.path.abspath(file.replace("$$$", "1")), format="mp3")
    # Play
    playsound.playsound(os.path.abspath(file.replace("$$$", "1")))

# speak(None,'Hello World, My name is cosmo')

# tts.py
# Text to speech implementation for reading the call information out loud
# Kyle Venenga


from gtts import gTTS
import gtts
from gtts.tokenizer import pre_processors
from playsound import playsound
import gtts.tokenizer.symbols
import time
import os
from tempfile import TemporaryFile
from googletrans import Translator
from pygame import mixer
import pygame, time

# build
# inputs a list of things to say [call type, addr, building type, description]
def build(ttsp, lang='en'):
    # Build the string
    text = ttsp[0] + " . call from . " + ttsp[1] + ". Building type is " + ttsp[2] + " . " + ttsp[3]

    # Initiate translator and mixer, create temp file
    translator = Translator()
    mixer.init()
    tf = TemporaryFile()

    # Add abbreviations to read
    gtts.tokenizer.symbols.SUB_PAIRS.append(('s.', 'south.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('w.', 'west.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('e.', 'east.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('n.', 'north.'))
    pre_processors.word_sub(text)

    # Create the text to speech object
    tts = gTTS(text=translator.translate(text, dest=lang).text, lang=lang)

    # Write to a temp file, then read and play
    tts.write_to_fp(tf)
    tf.seek(0)
    playsound("audio/tone.mp3")
    time.sleep(.35)
    mixer.music.load(tf)
    mixer.music.play()



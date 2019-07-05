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


def build(ttsp, lang='en'):
    text = ttsp[0] + " . call from . " + ttsp[1] + ". Building type is " + ttsp[2] + " . " + ttsp[3]
    print(text)
    translator = Translator()
    mixer.init()
    tf = TemporaryFile()
    gtts.tokenizer.symbols.SUB_PAIRS.append(('s.', 'south.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('w.', 'west.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('e.', 'east.'))
    gtts.tokenizer.symbols.SUB_PAIRS.append(('n.', 'north.'))
    pre_processors.word_sub(text)
    tts = gTTS(text=translator.translate(text, dest=lang).text, lang=lang)
    print(text)
    tts.write_to_fp(tf)
    tf.seek(0)
    playsound("audio/tone.mp3")
    time.sleep(.35)
    mixer.music.load(tf)
    mixer.music.play()



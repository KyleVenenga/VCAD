# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
import datetime
import math
import sys
from threading import Thread
from gtts import gTTS
import gtts
from gtts.tokenizer import pre_processors
from playsound import playsound
import gtts.tokenizer.symbols
import os
from tempfile import TemporaryFile
from googletrans import Translator
from pygame import mixer
import pygame, time
import pymysql
import cryptography

block_cipher = None


a = Analysis(['C:\\Users\\VeNinjaK\\Documents\\VCAD\\kv.py'],
             pathex=['C:\\Users\\VeNinjaK\\Documents\\VCAD\\Package'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='VCAD',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='VCAD')

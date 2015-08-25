#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Google TTS plugin
"""

from tempfile import NamedTemporaryFile
from gtts import gTTS
import pygame


class GoogleTTS(object):
    """
        Google TTS
    """
    def __init__(self, language):
        self.language = language

    def say(self, text):
        """
            Play text with stt + mplayer
        """
        with NamedTemporaryFile() as file_:
            gTTS(text=text, lang=self.language).write_to_fp(file_)

            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            pygame.mixer.music.load(file_.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(100)

            pygame.time.Clock().tick(100)

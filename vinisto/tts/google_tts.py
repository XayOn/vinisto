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
        with NamedTemporaryFile(delete=False) as file_:
            gTTS(text=text, lang=self.language).write_to_fp(file_)

            pygame.mixer.init(frequency=36000)
            pygame.mixer.music.load(file_.name)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)

            pygame.time.Clock().tick(10)

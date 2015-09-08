#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google STT plugin
"""

import speech_recognition as sr
import logging

logging.basicConfig(loglevel=logging.INFO)
LOG = logging.getLogger(__name__)


class GoogleSTT(object):
    """
        Google Speech recognition
    """
    def __init__(self, language, rate, key):
        self.language = language
        self.rate = rate
        self.chunk = rate / 2
        self.key = key

    def get_audio(self):
        """
            Return recognized text
        """
        rrec = sr.Recognizer('es-ES', self.key)
        mic = sr.Microphone()
        mic.RATE = self.rate
        mic.CHUNK = self.chunk
        with mic as source:
            LOG.info("Mic waiting")
            rrec.adjust_for_ambient_noise(source)
            return rrec.recognize(rrec.listen(source))

    @property
    def text(self):
        """
            Waits for text to be recognized, then yields it
        """
        while True:
            try:
                audio = self.get_audio()
                LOG.info("Recognized: %s", audio)
                yield audio.lower()
            except LookupError:
                pass

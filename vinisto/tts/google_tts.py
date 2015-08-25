#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Google TTS plugin
"""

from tempfile import NamedTemporaryFile
import subprocess
from gtts import gTTS
import os


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
            filename = file_.name
        subprocess.call(['mplayer', filename])
        os.unlink(filename)

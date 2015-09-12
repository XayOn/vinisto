#!/usr/bin/env python
# -*- coding: utf-8 -*-


from vinisto.i18n import _


"""
    Repeat
"""


class Repeat(object):
    """
        Repeats
    """
    def __init__(self, caller):
        self.caller = caller
        self.trigger = _('repeat')

    def callback(self, text):
        """
             cb
        """
        text = text.lower()
        if self.trigger in text:
            self.caller.tts.say(text.replace(self.trigger, ''))

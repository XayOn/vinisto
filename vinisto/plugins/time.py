#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from datetime import datetime
from vinisto.i18n import _


"""
    Time plugin.
    Speaks the time in spanish.
"""


class Time(object):
    """
        Simple plugin example
    """
    def __init__(self, caller):
        self.caller = caller
        self.trigger = [_(u'what time is it?'), _(u'It\'s {}')]

    def callback(self, text):
        """
             cb
        """
        trigger, response = self.trigger
        text = text.lower()

        if trigger in text:
            date_ = datetime.now().strftime(" %H %M %p").replace(" 0", " ")
            self.caller.tts.say(response.format(date_))

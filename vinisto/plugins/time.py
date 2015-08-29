#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from datetime import datetime
import locale


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
        self.triggers = {
            u'qué hora es': ['es_ES.utf-8', 'Son las {}'],
            'what time is it': ['en_US', 'It\'s {}']
        }

    def callback(self, text):
        """
             cb
        """
        for trigger, result in self.triggers.iteritems():
            text = text.lower()

            if trigger in text:
                locale.setlocale(locale.LC_TIME, result[0])
                date_ = datetime.now().strftime(" %H %M %p").replace(" 0", " ")
                time = result[1].format(date_)
                print(time)
                self.caller.tts.say(time)

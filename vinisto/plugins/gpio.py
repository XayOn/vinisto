#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    Control GPIO relays on raspberry pi
"""

RUN = True
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
except ImportError:
    RUN = False

from vinisto.i18n import _

VERBS = [_(u'Yes'), _(u'No')]


class Gpio(object):
    """
        Turn on/off GPIOs
    """
    def __init__(self, caller):
        self.caller = caller
        self.triggers = {
            _(u'Turn off the lights'):
                [12, GPIO.OUT, 1],
            _(u'Turn on the lights'):
                [12, GPIO.OUT, 0],
            _(u'Is there any light on?'):
                [14, GPIO.IN, lambda x: self.caller.tts.say(
                    VERBS[x])]
        }

    def callback(self, text):
        """
             cb
        """
        if not RUN:
            return

        text = text.lower()
        for trigger, data in self.triggers.items():
            if trigger in text:
                GPIO.setup(data[0], data[1])
                if data[1] == GPIO.OUT:
                    GPIO.output(data[0], data[2])
                else:
                    data[2](GPIO.input(data[0]))

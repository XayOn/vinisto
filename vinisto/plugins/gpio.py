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


VERBS = ['Si', 'No']


class Gpio(object):
    """
        Turn on/off GPIOs
    """
    def __init__(self, caller):
        self.caller = caller
        self.triggers = {
            'enciende la luz': [12, GPIO.OUT, 1],
            'apaga la luz': [12, GPIO.OUT, 0],
            'enciende la tetera': [13, GPIO.OUT, 1],
            'apaga la tetera': [13, GPIO.OUT, 0],
            'hay luz?': [14, GPIO.IN, lambda x: self.caller.tts.say(VERBS[x])]
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

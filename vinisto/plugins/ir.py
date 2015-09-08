#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    InfraRed
"""


import subprocess


class Repeat(object):
    """
        InfraRed module
        ---------------

        You need to have lirc configured.
        Then, associate:
            {
                'trigger': [ remote_control_name, press_key ]
            }
    """
    def __init__(self, caller):
        self.caller = caller
        self.triggers = {
            'pon la luz roja': ["control_luces", "roja"],
        }

    def callback(self, text):
        """
            callback
        """
        text = text.lower()
        for trigger, data in self.triggers.items():
            if trigger in text:
                subprocess.Popen(["irsend", "SEND_ONCE", data[0], data[1]])

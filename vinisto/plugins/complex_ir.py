#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    InfraRed
"""


from vinisto.i18n import _
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
            _(u'put the lights red'): ["light_control", "red"],
            _(u'turn the ac off'): ["ac_control", "key_0"],
        }

    def callback(self, text):
        """
            callback
        """
        text = text.lower()
        for trigger, data in self.triggers.items():
            if trigger in text:
                subprocess.Popen(["irsend", "SEND_ONCE", data[0], data[1]])

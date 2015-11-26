#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    InfraRed
    This plugin:
"""


from vinisto.i18n import _
import markovify
import os

MDB = os.path.expanduser('~/.vinisto_markov')
MARKOV = markovify.Text(open(MDB).read())


class Markov(object):
    """
    """
    def __init__(self, caller):
        self.caller = caller
        self.triggers = [_("Tell me something")]

    def callback(self, text):
        """
            callback
        """
        for trigger in self.triggers:
            if trigger in text:
                return self.caller.tts.say(MARKOV.make_sentence())

        with open(MDB, 'a') as mf:
            mf.write("{}\n".format(text))

        global MARKOV
        MARKOV = markovify.Text(open(MDB).read())

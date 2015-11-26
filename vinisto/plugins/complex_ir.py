#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    InfraRed
    This plugin:
"""


from vinisto.i18n import _, TAGGER
import subprocess
import pexpect
import re
import os

LIRC_FILE = os.path.expanduser("~/.vinisto_lirc.cfg")


def read_lirc_file(lirc_file):
    """
        Reads a LIRC config file
        and extrats the remotes and buttons =)
    """

    def make_groups(lines, start, end, name):
        """
            Generic grouping.
            Gets a file in the form

            start
            asdfasdf
            asdfasdf
            end
            start
            123123123
            123123123
            end

            and returns groups (asdfasdf, asdfasdf), (123123123, 123123123)
        """
        starts = []
        ends = []

        for n, line in enumerate(lines):
            if "{} {}".format(start, name) in line:
                starts.append(n)
            elif "{} {}".format(end, name) in line:
                ends.append(n)
        return zip(starts, ends)

    def clean(phrase):
        """
            Cleanses spaces
        """
        return re.sub('\s+', ' ', phrase).strip().split(" ")[0]

    with open(lirc_file) as file_:
        lines = [a for a in file_.readlines() if a.strip()]
        res = {}
        for (x, y) in make_groups(lines, 'begin', 'end', 'remote'):
            for (x_, y_) in make_groups(lines[x:y], 'begin', 'end', 'codes'):
                for (xn, yn) in make_groups(lines[x:y], 'name', '', ''):
                    name = lines[x:y][xn:yn+2][0].replace('name', '').strip()
                    break
                res[name] = [clean(a) for a in lines[x:y][x_+1:y_]]

        return res


class IR(object):
    """
    """
    def __init__(self, caller):
        self.caller = caller
        self.remotes = read_lirc_file(LIRC_FILE)
        self.configure_command = _("Nuevo mando")

    def reload_remotes(self):
        self.remotes = read_lirc_file(LIRC_FILE)

    def save_remotes(self):
        return

    def exec_remote(self, remote, command):
        """
            Call irsend
        """
        return subprocess.Popen(["irsend", "SEND_ONCE", remote, command])

    def configure_new_remote(self, remote_name):
        pe = pexpect.check_call('irrecord --ignore-namespace {}'.format(
            LIRC_FILE))
        pe.expect('Don\'t stop pressing buttons')
        self.caller.tts.say(_("""We're going to configure your remote now.
                              Reserved words for buttons are cancel and done.
                              Please, keep pressing buttons (a second each)
                              for half a minute, until I tell you to stop."""))
        pe.sendline()
        pe.expect('Found')
        self.caller.tts.say(_("""Please, continue pressing buttons as before, we are almost
                              there"""))
        pe.sendline()

        self.caller.tts.say(_("""You can stop pressing buttons now.
                              Now we're going to record the buttons.
                              When you're finished with them, say done.

                              Tell me the trigger phrase of the first button
                              to configure

                              After each button, I'll tell you what I've
                              recognized.

                              I will interpret everything as close as possible
                              to reality.

                              If I have not correctly recognized your button,
                              you can say cancel to retry.
                              """))

        while True:
            action = next(self.caller.stt.text)
            if action == _("cancel"):
                continue
            if action == _("done"):
                pe.sendline()
                pe.sendline()
                break

            tags = TAGGER.get_main_words(action, lemmatize=True,
                                         type_w=["W", "N"])

            button = '_'.join(tags)

            pe.sendline(button)
            pe.expect("Now hold down")
            self.caller.tts.say(_("""Now press the button"""))

        return subprocess.Popen()

    def callback(self, text):
        """
            callback
        """
        if self.configure_command in text:
            text = TAGGER.get_main_words(
                text.replace(self.configure_command, ''),
                lemmatize=True, type_w=["N", "X"])

            # Sorry, only the first noun =P
            # this way we can use complex phrasing and still
            # make it work. Like 'Add a new remote called Balls'
            # And unknown names, as 'Add a new remote called MyBalls'
            # =)

            self.configure_new_remote(text[0])
            self.reload_remotes()
            return

        text = TAGGER.get_main_words(text, lemmatize=True,
                                     type_w=['W', "N"])
        for remote, buttons in self.remotes:
            for button in buttons:
                tags = TAGGER.get_main_words(button.split('_'),
                                             lemmatize=True,
                                             type_w=["W", "N"])
                if tags == text:
                    # And yes, with this code you could accidentally make
                    # make the same button on different remotes
                    # without really realising it... need to make
                    # it into the docs =P
                    self.exec_remote(remote, button)

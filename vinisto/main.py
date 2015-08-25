#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Main
"""

import logging


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Vinisto(object):
    """
        Vinisto
    """
    def __init__(self):
        self.plugins = []
        self.stt = False
        self.tts = False

    def register_plugin(self, plugin):
        """
            Register a plugin
        """
        self.plugins.append(plugin(self))

    def execute_callbacks(self):
        """
            Launch callback function on all registered plugins
        """
        try:
            text = next(self.stt.text)
        except LookupError:
            pass
        for plugin in self.plugins:
            try:
                plugin.callback(text)
            except:
                # We can't allow a bad plugin to break anything =(
                pass


def main():
    """
        Usually this should not be used,
        you must implement this part yourself.

        Have a nice day =)
    """

    from vinisto.tts.google_tts import GoogleTTS
    from vinisto.stt.google_stt import GoogleSTT
    from vinisto.plugins.time import Time
    from vinisto.plugins.repeat import Repeat

    vinisto = Vinisto()
    vinisto.stt = GoogleSTT('es-ES', {'rate': 24000},
                            "AIzaSyCuOvb2qd0mhQRkIbGAcgMUmFQaLIXtlmg")
    vinisto.tts = GoogleTTS('es-ES')
    vinisto.register_plugin(Time)
    vinisto.register_plugin(Repeat)
    while True:
        vinisto.execute_callbacks()


if __name__ == "__main__":
    main()

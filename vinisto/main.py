#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Main
"""

import inspect
import logging
import pkgutil
import argparse
import vinisto.plugins
import vinisto.tts
import vinisto.stt
from importlib import import_module


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
        LOG.info("Registering plugin {}".format(plugin))
        self.plugins.append(plugin(self))

    def wait_for_keyword(self, keyword):
        while True:
            LOG.info("Wating for keyword")
            if next(self.stt.text) == keyword:
                break

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
                LOG.info('Calling plugin {} callback'.format(plugin))
                plugin.callback(text)
            except:
                # We can't allow a bad plugin to break anything =(
                pass


def extract_modules(module, nam):
    """
        Get vinisto modulenames for a specific submodule.
    """
    modules = pkgutil.iter_modules(module.__path__)
    return ["vinisto.{}.{}".format(nam, mod) for _, mod, _ in modules]


def extract_classes(plugins):
    """
        Extracts all classes in
    """
    for module in plugins:
        try:
            module = import_module(module)
            for class_ in inspect.getmembers(module, inspect.isclass):
                if class_[1].__module__.startswith('vinisto.'):
                    yield class_[1]
        except RuntimeError:
            pass


def main():
    """
        Main CLI.
        This receives as parameters the vinisto modules to load.
    """
    vinisto_ = Vinisto()

    plugins = extract_modules(vinisto.plugins, 'plugins')
    tts_plugins = extract_modules(vinisto.tts, 'tts')
    stt_plugins = extract_modules(vinisto.stt, 'stt')

    parser = argparse.ArgumentParser(
        description='Vinisto - Your personal butler')

    parser.add_argument('--plugins',  type=str, nargs='?',
                        choices=plugins,
                        help='List of plugin modules',
                        default=plugins)

    parser.add_argument('--stt',  type=str,
                        choices=stt_plugins,
                        help='List of stt modules',
                        default='vinisto.stt.google_stt')

    parser.add_argument('--tts',  type=str,
                        choices=tts_plugins,
                        help='List of tts modules',
                        default='vinisto.tts.google_tts')

    parser.add_argument('--keyword',  type=str,
                        help='Keyword to wait for',
                        default='vinisto')

    args = parser.parse_args()

    TTS = next(extract_classes([args.tts]))
    STT = next(extract_classes([args.stt]))

    vinisto_.stt = STT(language='es-ES', rate=24000,
                       key="AIzaSyCuOvb2qd0mhQRkIbGAcgMUmFQaLIXtlmg")
    vinisto_.tts = TTS(language='es-ES')

    for class_ in extract_classes(plugins):
        vinisto_.register_plugin(class_)

    while True:
        vinisto_.wait_for_keyword(args.keyword)
        LOG.info("Keyword recognized")
        vinisto_.execute_callbacks()


if __name__ == "__main__":
    main()

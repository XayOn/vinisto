#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Main
"""

import inspect
import locale
import pkgutil
import argparse
import vinisto.plugins
import vinisto.tts
import vinisto.stt
from vinisto.i18n import _
from vinisto import LOG
from importlib import import_module
from threading import Thread


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
            LOG.info("Wating for keyword {}".format(keyword))
            text = next(self.stt.text)
            LOG.info(u"GOT {}".format(text))

            if text == keyword:
                LOG.info("Yielding false, only keyword found")
                yield False
            elif keyword in text:
                LOG.info("Yielding text {}".format(text.replace(keyword, '')))
                yield text.replace(keyword, '')

    def execute_callbacks(self, text=False):
        """
            Launch callback function on all registered plugins
            We can provide a text to be evaluated.
        """
        if not text:
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
                        help='Keyword to wait for')

    parser.add_argument('--rate', type=str,
                        help="Mic rate, defaults to raspberry pi USB (24000)",
                        default=24000)

    parser.add_argument('--language', type=str,
                        help="Language to use in both TTS and STT",
                        default=locale.getdefaultlocale()[0].replace('_', '-'))

    parser.add_argument('--key', type=str,
                        help="Key to be passed to STT engines.",
                        default="AIzaSyCuOvb2qd0mhQRkIbGAcgMUmFQaLIXtlmg")

    parser.add_argument('--response_phrase', type=str,
                        help="What to say when the keyword has been detected")

    args = parser.parse_args()

    TTS = next(extract_classes([args.tts]))
    STT = next(extract_classes([args.stt]))

    vinisto_.stt = STT(language=args.language, rate=args.rate,
                       key=args.key)
    vinisto_.tts = TTS(language=args.language)

    for class_ in extract_classes(plugins):
        vinisto_.register_plugin(class_)

    keyword = _(u'vinisto')
    phrase = _(u'Yes, master?')

    if args.keyword:
        keyword = args.keyword

    if args.response_phrase:
        phrase = args.response_phrase

    phrases = vinisto_.wait_for_keyword(keyword.lower())

    for text in phrases:
        LOG.info("Received: %s", text)
        if not text:
            LOG.info("Asking tts to say our phrase")
            Thread(target=vinisto_.tts.say, args=(phrase,)).start()
        LOG.info("Going to execute callbacks now:")
        LOG.info('-------------------------------')
        vinisto_.execute_callbacks(text)


if __name__ == "__main__":
    main()

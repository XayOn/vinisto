Vinisto
-------

Vinisto is the word for "butler" in `Esperanto <https://en.wikipedia.org/wiki/Esperanto>`_.

It's based on the following main directrives:

    - It has to be easy to expand
    - Non-strict, you may do as you please
    - Support many tts/stt systems
    - Multilanguage
    - KISS

But mostly, KISS is the most important one.

Installation
------------

This requires pyaudio.
I recommend installing pyaudio from your package manager
It also requires pygame, wich requires the same treatment.

IE debian:

::

    apt-get install python-pyaudio python-pygame

After that, pip install vinisto will do the magic.

Executing vinisto
-----------------

Vinisto is ready to use as a library, wich is it's main goal, but you can try
with some default plugins (time and repeat) by using the built-in "vinisto"
command

::

    usage: vinisto [-h]
                   [--plugins [{vinisto.plugins.gpio,vinisto.plugins.repeat,vinisto.plugins.time}]]
                   [--stt {vinisto.stt.google_stt}]
                   [--tts {vinisto.tts.google_tts}] [--keyword KEYWORD]
                   [--rate RATE] [--language LANGUAGE] [--key KEY]

    Vinisto - Your personal butler

    optional arguments:
      -h, --help            show this help message and exit
      --plugins [{vinisto.plugins.gpio,vinisto.plugins.repeat,vinisto.plugins.time}]
                            List of plugin modules
      --stt {vinisto.stt.google_stt}
                            List of stt modules
      --tts {vinisto.tts.google_tts}
                            List of tts modules
      --keyword KEYWORD     Keyword to wait for
      --rate RATE           Mic rate, defaults to raspberry pi USB (24000)
      --language LANGUAGE   Language to use in both TTS and STT
      --key KEY             Key to be passed to STT engines.



wich WAS (now it handles arguments, but still...) basically

::

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



Expanding vinisto
-----------------

Vinisto has a simple-yet-effective structure, a main package with packages for
each of the principal functionalities:

    - tts
    - stt
    - plugins

Previous usage example is perfect to illustrate how to use them.
And `vinisto.tts.google_tts` for the tts part,
`vinisto.stt.google_stt` for the stt part and finally
`vinisto.plugins.time` for the plugins part


Using vinisto
-------------

Vinisto waits for a keyword "vinisto" (that can be changed on main.py).
After that, it'll receive one phrase, and will try to execute it.

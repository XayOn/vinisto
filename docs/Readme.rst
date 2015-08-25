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
I recommend installing pyaudio from your package manager, IE in debian

::

    apt-get install python-pyaudio

After that, pip install vinisto will do the magic.

Executing vinisto
-----------------

Vinisto is ready to use as a library, wich is it's main goal, but you can try
with some default plugins (time and repeat) by using the built-in "vinisto"
command

::

    vinisto

wich is basically

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import locale
import gettext
from vinisto.i18n.tokenizer import Tagger
from vinisto import __PATH__, __APP_NAME__

LOCALE_DIR = os.path.join(__PATH__, 'i18n')

gettext.bind_textdomain_codeset(__APP_NAME__, "UTF-8")
language = gettext.translation(__APP_NAME__, LOCALE_DIR, fallback=False)

LANG = locale.getdefaultlocale()[0]

if LANG.startswith('EN'):
    TAGGER = Tagger('brown')
elif LANG.startswith('ES') or LANG == "C":
    TAGGER = Tagger('cess_esp')
else:
    TAGGER = Tagger('brown')  # TODO: make this able to fail.

_ = language.ugettext

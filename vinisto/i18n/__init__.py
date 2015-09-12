#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gettext

from vinisto import __PATH__, __APP_NAME__

LOCALE_DIR = os.path.join(__PATH__, 'i18n')

gettext.bind_textdomain_codeset(__APP_NAME__, "UTF-8")
language = gettext.translation(__APP_NAME__, LOCALE_DIR, fallback=False)

_ = language.ugettext

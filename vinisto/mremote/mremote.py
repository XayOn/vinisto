#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask based API.
    Requires ircsend to work.
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from scipy.spatial import distance
import subprocess
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
CONF_FILE = os.path.join("/etc/lirc/lircd.conf")


BUTTONS = json.dumps(read_lirc_file())
APP = Flask(__name__, template_folder=TEMPLATES_DIR)
Bootstrap(APP)


@APP.route('/')
def index():
    return render_template('index.html', buttons=BUTTONS)


@APP.route('/action/<remote>/<action>')
def action(remote, action_):
    """
        Executes a custom action.
    """
    result = subprocess.check_call(['irsend', 'SEND_ONCE', remote, action_])
    return json.dumps({"key": action_, 'result': result})


def main():
    """
        Run app
    """
    APP.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    main()

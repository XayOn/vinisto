"""
Configuration management

"""

# pylint: disable=invalid-name

import configparser

config = configparser.ConfigParser()
config.read('~/.vinisto.conf')

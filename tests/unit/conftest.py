"""
Conftest
"""

import pytest


@pytest.fixture
def config():
    """
    Mocked config
    """

    from unittest.mock import patch
    from configparser import ConfigParser

    config_mock = ConfigParser()
    config_mock.add_section("main")
    config_mock.set("main", "mqtt_template", "")
    config_mock.set("main", "", "")
    config_mock.add_section("speech")
    config_mock.set("speech", "microphone_name", "basic_microphone")
    return patch('vinisto.config', return_value=config_mock)


@pytest.fixture
def test_feature():
    import os
    rules_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "fixtures"))
    return [open("{}/rules/test_rule.feature".format(rules_dir)).read()]

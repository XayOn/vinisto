"""
Connector to vinisto REST API
"""

import json
from vinisto.config import config
import requests


class RestConnector:
    """
    Rest connector to main api
    """
    url = "http://{}:{}/{{}}".format(
        config.get("api", "ip"), config.get("api", "port"))

    @staticmethod
    def send_messages(msg):
        """ Send sensors messages to vinisto API """
        return requests.post(
            RestConnector.url.format('sensor'),
            data={k: v for k, v in json.loads(msg).items()})

    @staticmethod
    def execute_step(msg):
        """ Directly call for a step execution """
        return requests.post(
            RestConnector.url.format('execute_step'),
            data={"step": msg})

"""
Connector to vinisto REST API
"""

import json
from vinisto.config import config
import requests


def send_messages(msg):
    """ Send sensors messages to vinisto API """
    url = "http://{}:{}/sensor".format(
        config.get("api", "ip"), config.get("api", "port"))
    return requests.post(url, data={k: v for k, v in json.loads(msg).items()})

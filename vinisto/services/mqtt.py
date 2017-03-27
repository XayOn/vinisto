"""
Vinisto mqtt direct integration.
Probably to be deprecated
"""
import json

from vinisto.utils import mqtt_client
from vinisto.config import config
import requests


def send_messages(msg):
    """ Send sensors messages to vinisto API """
    url = "http://{}:{}/sensor".format(
        config.get("api", "ip"), config.get("api", "port"))
    return requests.post(url, data={k: v for k, v in json.loads(msg).items()})


def mqtt_to_rest():
    """Connect to the mqtt server and send every sensor event to the API"""

    def setup_client(client):
        """ Setup the mqtt client """
        client.engine.mqtt = client
        client.on_message = lambda c, _, msg: send_messages(msg)
        client.on_disconnect = lambda c, u, r: c.reconnect()

    mqtt_client(setup_client)

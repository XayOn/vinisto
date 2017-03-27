"""
Vinisto mqtt direct integration.
Probably to be deprecated
"""
import json

from vinisto.engine import VinistoEngine
from vinisto.utils import mqtt_client
from vinisto.config import config


def mqtt_consumer(features):
    """
    Connect to the mqtt server and act upon each message received
    on the configured queue.
    """

    def setup_client(client):
        """
        Setup a consumer client with a VinistoEngine execution each time
        it receives a message.
        """
        context = {"rules": [], "final_rules": [],
                   "mqtt_template": config.get('main', 'mqtt_template')}
        client.engine = VinistoEngine(features=features, context=context)
        client.engine.mqtt = client
        client.on_message = lambda c, _, msg: c.engine.receive(
            json.loads(msg.payload.decode('utf-8')))
        client.on_disconnect = lambda c, u, r: c.reconnect()

    mqtt_client(setup_client)

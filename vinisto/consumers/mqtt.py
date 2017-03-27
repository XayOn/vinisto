"""
Vinisto mqtt direct integration.
Probably to be deprecated
"""
import json

import paho.mqtt.client as mqtt
from vinisto.config import config
from vinisto.engine import VinistoEngine


def main(features):
    """
    Connect the mqtt server
    """

    context = {"rules": [], "final_rules": [],
               "mqtt_template": config.get('main', 'mqtt_template')}
    mqtt_config = dict(config.items("mqtt"))
    subscription = mqtt_config.pop("subscription_path")

    def load(msg):
        """ Load a json message """
        return json.loads(msg.payload.decode('utf-8'))

    client = mqtt.Client("automation")
    client.engine = VinistoEngine(features=features, context=context)
    client.engine.mqtt = client
    client.on_message = lambda c, _, msg: c.engine.update_sensors(load(msg))
    client.on_disconnect = lambda c, u, r: c.reconnect()
    client.connect(**mqtt_config)
    client.subscribe(subscription)
    client.loop_forever()

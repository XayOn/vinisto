"""
Utils
"""

import paho.mqtt.client as mqtt
from vinisto.config import config


def mqtt_client(setup_client=lambda c: c):
    """
    MQTT client
    """
    mqtt_config = dict(config.items("mqtt"))
    subscription = mqtt_config.pop("subscription_path")
    client = mqtt.Client("automation")
    setup_client(client)
    client.connect(**mqtt_config)
    client.subscribe(subscription)
    client.loop_forever()

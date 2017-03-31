"""
Vinisto mqtt direct integration.
Probably to be deprecated
"""

from json import loads
import paho.mqtt.client as mqtt
from vinisto import config
from vinisto.services import RestConnector


def run():
    """Connect to the mqtt server and send every sensor event to the API"""
    connector = RestConnector()

    mqtt_config = dict(config.items("mqtt"))
    mqtt_config['port'] = int(mqtt_config['port'])
    topics = mqtt_config.pop("topics").split(',')

    client = mqtt.Client()
    client.on_message = lambda c, _, m: connector.update_sensors(
        loads(m.payload.decode('utf-8')))
    client.on_disconnect = lambda c, u, r: c.reconnect()
    client.on_connect = lambda c, u, f, r: [c.subscribe(t) for t in topics]
    client.connect(**mqtt_config)
    client.loop_forever()

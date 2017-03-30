"""
Vinisto mqtt direct integration.
Probably to be deprecated
"""

from vinisto.utils import mqtt_client
from vinisto.services import RestConnector


def run():
    """Connect to the mqtt server and send every sensor event to the API"""
    connector = RestConnector()

    def setup_client(client):
        """ Setup the mqtt client """
        client.engine.mqtt = client
        client.on_message = lambda c, _, msg: connector.update_sensors(msg)
        client.on_disconnect = lambda c, u, r: c.reconnect()

    mqtt_client(setup_client)

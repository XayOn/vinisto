"""
Connector to vinisto REST API
"""

from gettext import gettext as _
from potion_client import Client
from vinisto import config


class RestConnector:
    """ Rest connector to main api """

    def __init__(self):
        self.url = "http://{}:{}".format(config.get("api", "ip"),
                                         config.get("api", "port"))
        self.client = Client(self.url)
        self.template = _("""Feature: voice recognition
                             Scenario: I received a voice command
                                       When I receive a voice command
                                       Then {}""")

    def update_sensors(self, sensors):
        """ Update sensor values """
        for name, value in sensors.items():
            sensor = self.client.Sensor.first(where={"name": name})
            sensor.value = str(value)
            sensor.save()

    def execute_then(self, step):
        """ Directly call for a step execution """
        feature = self.template.format(step)

        try:
            feat = self.client.Feature.create(text=feature)
        except:
            feat = self.client.Feature.first(text=feature)

        feat.execute()

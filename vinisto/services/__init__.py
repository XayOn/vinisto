"""
Connector to vinisto REST API
"""

from potion_client import Client
from vinisto.config import config
import requests


class RestConnector:
    """ Rest connector to main api """

    def __init__(self):
        self.url = "http://{}:{}/".format(config.get("api", "ip"),
                                     config.get("api", "port"))
        self.client = Client(url)

    @staticmethod
    def update_sensors(sensors):
        """ Update sensor values """
        for name, value in sensors:
            sensor = self.client.User.first(where={"name": name})
            sensor.value = value
            sensor.save()

    @staticmethod
    def execute_step(msg):
        """ Directly call for a step execution """
        return requests.post("{}{}".format(self.url, '/execute_step'),
                             data={"step": msg})

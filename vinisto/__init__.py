""" Basic API """

import configparser
from vinisto.models import Feature
from vinisto.models import Sensor
from flask_potion import Api, ModelResource, signals, fields
from flask_potion.routes import ItemRoute
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask

# pylint: disable=no-member, invalid-name


APP = Flask(__name__)

config = configparser.ConfigParser()
config.read('~/.vinisto.conf')


class FeatureResource(ModelResource):
    """ Features """
    @ItemRoute.GET('/execute')
    def execute(self, feature) -> fields.Boolean():
        """ Execute a given feature """
        # pylint: disable=no-self-use
        Feature.get_engine([feature]).run()
        return True

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        model = Feature


class SensorResource(ModelResource):
    """ Sensors """
    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        model = Sensor


@signals.after_update.connect_via(SensorResource)
def sensor_updated(_, item, changes):
    """ Run the KE on sensor update if the value has changed """
    if "value" in changes.keys():
        APP.config['engine'].receive({item.name, item.value})


def run():
    """ Run server """
    APP.config['engine'] = Feature.get_engine(Feature.select())
    api = Api(APP, default_manager=PeeweeManager)
    api.add_resource(FeatureResource)
    api.add_resource(SensorResource)

    if __name__ == '__main__':
        APP.run()

if __name__ == "__main__":
    run()

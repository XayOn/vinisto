""" Basic API """

import os
from vinisto.models import Feature
from vinisto.models import Sensor
from flask_potion import Api, ModelResource, signals, fields
from flask_potion.routes import ItemRoute
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask

APP = Flask(__name__)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


@APP.route("/")
def index():
    return open(os.path.join(TEMPLATES_DIR, 'index.html')).read()


class FeatureResource(ModelResource):
    @ItemRoute.GET('/execute')
    def execute(self, feature) -> fields.Boolean():
        Feature.get_engine([feature]).run()
        return True

    class Meta:
        model = Feature


class SensorResource(ModelResource):
    class Meta:
        model = Sensor


@signals.after_update.connect_via(SensorResource)
def sensor_updated(sender, item, changes):
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

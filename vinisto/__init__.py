""" Basic API """

from vinisto.models import Feature
from vinisto.models import Sensor
from flask_potion import Api, ModelResource
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask

APP = Flask(__name__)


@APP.route("/")
def index(request):
    return open('./templates/index.html').read()


class FeatureResource(ModelResource):
    class Meta:
        model = Feature


class SensorResource(ModelResource):
    class Meta:
        model = Sensor


def run():
    """ Run server """
    api = Api(APP, default_manager=PeeweeManager)
    api.add_resource(FeatureResource)
    api.add_resource(SensorResource)

    if __name__ == '__main__':
        APP.run()


if __name__ == "__main__":
    run()

"""
Basic API
"""


from vinisto.models import FeatureModel as Feature
from vinisto.models import SensorModel as Sensor
from flask_peewee.rest import RestAPI
from flask import Flask

app = Flask(__name__)
api = RestAPI(app)
api.register(Feature)
api.register(Sensor)
api.setup()

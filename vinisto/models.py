"""
Models
"""

from functools import lru_cache
import peewee
from vinisto.config import config


@lru_cache()
def get_database():
    """ Get database """
    dbconfig = dict(config.items("database"))
    dbname = dbconfig.pop('name')
    dbtype = dbconfig.pop('type')
    database = getattr(peewee, dbtype)(dbname, **dbconfig)
    database.set_allow_sync(False)
    return database


class FeatureModel(peewee.Model):
    """ Feature Model """

    base = peewee.TextField()
    variables = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = get_database()


class SensorModel(peewee.Model):
    """ Sensor Model """

    name = peewee.TextField()
    value = peewee.TextField()
    http_verb = peewee.TextField()
    url_template = peewee.TextField()
    data_template = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = get_database()

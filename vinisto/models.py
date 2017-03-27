"""
Models
"""

from functools import lru_cache
import peewee
import peewee_async
from vinisto.config import config


@lru_cache()
def get_database():
    """ Get database """
    dbconfig = dict(config.items("database"))
    dbname = dbconfig.pop('name')
    database = peewee_async.MySQLDatabase(dbname, **dbconfig)
    database.set_allow_sync(False)
    return database


@lru_cache()
def get_objects():
    """ Return object manager for given database """

    return peewee_async.Manager(get_database())


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

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = get_database()

"""
Models
"""

import peewee

DATABASE = peewee.SqliteDatabase("temp")


class Feature(peewee.Model):
    """ Feature Model """

    text = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DATABASE

    @staticmethod
    def get_engine(select):
        """
        Return engine
        """
        from vinisto.engine import VinistoEngine
        return VinistoEngine(
            base_context={"final_rules": [], "rules": []},
            features_list=[a.text for a in select])


class Sensor(peewee.Model):
    """ Sensor Model """

    update_types = ["button", "slider"]
    name = peewee.TextField()
    type = peewee.TextField()
    value = peewee.TextField(null=True)

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DATABASE

    def remote_update(self):
        """
        If this is a reactor against a remote REST API, launch the
        request.
        """
        # pylint: disable=no-member
        if self.type not in self.update_types:
            return False

        # TODO: Publish it via MQTT.

DATABASE.create_tables([Sensor, Feature], safe=True)

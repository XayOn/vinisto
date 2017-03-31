"""
Models
"""

import json
import peewee
import requests

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
    http_verb = peewee.TextField(null=True)
    url_template = peewee.TextField(null=True)
    reacts = peewee.BooleanField(null=True)
    data_template = peewee.TextField(null=True)

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DATABASE

    def remote_update(self):
        """
        If this is a reactor against a remote REST API, launch the
        request.
        """
        # pylint: disable=no-member
        if not self.reacts:
            return False

        data = {}
        if self.data_template:
            data = json.loads(self.data_template.format(
                    name=self.name, value=self.value))

        try:
            return getattr(requests, self.http_verb)(
                self.url_template.format(name=self.name, value=self.value),
                data=data)
        except Exception as err:
            print(err)


DATABASE.create_tables([Sensor, Feature], safe=True)

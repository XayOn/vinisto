""" REST consumers """


from functools import lru_cache
import json
import operator
import requests

from vinisto.abstract import AbstractEmitter
from vinisto.models import FeatureModel, SensorModel
from vinisto.engine import VinistoEngine

from aiohttp import web


# pylint: disable=too-few-public-methods
class VinistoRestProducer(metaclass=AbstractEmitter):
    """ Vinisto rest producer """
    model = SensorModel

    # pylint: disable=no-self-use
    def emit(self, key, value):
        """ Emit to a REST api """
        obj = SensorModel.get(name=key)
        return getattr(requests, obj.http_verb)(
            obj.url_template.format(name=key, value=value),
            data=json.loads(obj.data_template.format(name=key, value=value)))


class BasicREST(web.View):
    """ Basic REST API, just implementing what I need here.  """

    def modelify(self, data_dict):
        """ Small hack to convert a dict to a select query """
        for key, value in data_dict.items():
            yield operator.eq(getattr(self.model, key), value)

    async def post(self):
        """ Create a new object """
        return web.json_response(self.model.create(**self.request.post()))

    async def get(self):
        """ Read either all objects or the query specified by the router """
        return web.json_response(self.model.get(
            *self.modelify(dict(self.request.match_info))))

    async def patch(self):
        """ Update/Modify object """
        obj = self.model.get(*self.modelify(self.request.match_info))
        for key, value in (await self.request.post()).items():
            setattr(obj, key, value)
        return web.json_response(await self.objects.update(obj))

    async def delete(self):
        """ Delete an object by id """
        return web.json_response(self.model.get(
            *self.modelify(self.request.match_info))).delete()


class VinistoSensorsConsumerView(BasicREST):
    """ Basic REST Sensor API """

    model = SensorModel

    async def post(self):
        """ Received a sensor value, save it in the db and exec the KE """
        super().post()
        # pylint: disable=no-member
        self.engine.receive(**self.request.post())


class VinistoFeaturesConsumerView(BasicREST):
    """ Basic REST Features API """
    model = FeatureModel


def vinisto_rest_consumer():
    """
    Vinisto REST consumer
    """
    engine = VinistoEngine(
        base_context={"final_rules": [], "rules": []},
        features_list=[a.base.format(a.variables) for a in
                       FeatureModel.select()],
        emitter=VinistoRestProducer)
    VinistoFeaturesConsumerView.engine = engine

    app = web.Application()
    app.router.add('/feature', VinistoFeaturesConsumerView)
    app.router.add('/sensor', VinistoSensorsConsumerView)
    app.run()

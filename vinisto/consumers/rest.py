""" REST consumers """

from functools import lru_cache

from vinisto.models import FeatureModel, SensorModel, get_objects
from vinisto.producers.rest import VinistoRestProducer
from vinisto.engine import VinistoEngine

from aiohttp import web


class BasicREST(web.View):
    """ Basic REST API, just implementing what I need here.  """
    objects = get_objects()

    async def post(self):
        """ Create a new object """
        return web.json_response(
            await self.objects.create(**await self.request.post()))

    async def get(self):
        """ Read either all objects or the query specified by the router """
        return web.json_response(await self.objects.get(
            **dict(self.request.match_info)))

    async def patch(self):
        """ Update/Modify object """
        obj = await self.objects.get(**dict(self.request.match_info))
        for key, value in (await self.request.post()).items():
            setattr(obj, key, value)
        return web.json_response(await self.objects.update(obj))

    async def delete(self):
        """ Delete an object by id """
        return web.json_response(await self.objects.delete(
            **dict(self.request.match_info)))


class VinistoSensorsConsumerView(BasicREST):
    """ Basic REST Sensor API """

    model = SensorModel

    @lru_cache()
    @property
    def engine(self):
        """ Return a freshly produced vinisto engine. """
        return VinistoEngine(
            base_context={"final_rules": [], "rules": []},
            features_list=[],
            emitter=VinistoRestProducer)

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
    app = web.Application()
    app.router.add('/feature', VinistoFeaturesConsumerView)
    app.router.add('/sensor', VinistoSensorsConsumerView)
    app.run()

"""
Vinisto Knowledge Engine.
"""
import string
from random import choice
from copy import deepcopy

from behave.configuration import Configuration
from behave.parser import parse_feature
from behave.runner import Runner, Context
from pyknow import KnowledgeEngine

from vinisto.facts import Sensor


class VinistoKE(KnowledgeEngine):
    """
    Custom KnowledgeEngine
    """
    def update_sensors(self, sensors):
        """
        Update sensor values:

        - Retract previous values of the same sensor.
        - Declare new ones

        This is probably a bad idea, since already-declared
        things will trigger changes on each message.

        Wich means... don't touch things manually while using vinisto.
        And have all your actions have an state (for example, use "turn on"
        instead of "toggle").

        This is kind of a problem since that means I can't turn the tv with
        this method, unless I make some kind of internal state for
        stateless triggers...
        """

        assert isinstance(sensors, dict)
        for key, _ in sensors.items():
            self.retract_matching(Sensor(name=key))
        self.declare(*(Sensor(name=k, value=v) for k, v in sensors.items()))
        self.run()


class VinistoEngine:
    """
    Vinisto Knowledge Engine class
    """
    # pylint: disable=too-few-public-methods

    def __new__(cls, **kwargs):
        def _random_name():
            return ''.join(choice(string.ascii_uppercase) for _ in range(10))

        engine_cls = type(
            "Engine", (VinistoKE,),
            {_random_name(): rule for rule in cls.get_rules(**kwargs)})

        engine = engine_cls()
        engine.reset()
        return engine

    @staticmethod
    def get_rules(features_list, base_context):
        """ Execute gherkins and return rules """

        runner = Runner(Configuration())

        for data in features_list:
            context_copy = deepcopy(base_context)
            context = Context(runner)
            for key, value in context_copy.items():
                setattr(context, key, value)
            runner.context = context
            parse_feature(data, None, None).run(runner)
            if runner.undefined_steps:
                raise Exception("Undefined {}".format(runner.undefined_steps))
            yield from context.final_rules

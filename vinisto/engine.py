"""
Vinisto Knowledge Engine.
"""

# pylint: disable=no-name-in-module

import string
from copy import deepcopy
from gettext import gettext as _
from random import choice

from behave import when, then, given
from behave.configuration import Configuration
from behave.parser import parse_feature
from behave.runner import Runner, Context

from pyknow import KnowledgeEngine
from pyknow import Rule, AND, L, P
from pyknow.fact import Fact

from vinisto.models import Sensor


class SensorFact(Fact):
    pass


@given(_("I have a sensor {name}"))
def add_sensor(context, name):
    Sensor.get_or_create(name=name, type="sensor")


@given(_("I have a {type} {name} that reacts on {http_verb}"
         " to {url_template} with {data_template}"))
def add_reactor(context, name, type, http_verb, url_template, data_template):
    """ Add a reactor-type sensor """
    Sensor.get_or_create(name=name, type=type, http_verb=http_verb,
                         url_template=url_template,
                         data_template=data_template)


@when(_("sensor {sensor} has value {value}"))
def sensor_has_value(context, sensor, value):
    """ When we receive a fact that the sensor has a specific value """
    sensor = sensor.replace(' ', '_')
    context.rules.append(SensorFact(name=sensor, value=L(value)))


@when(_("sensor {sensor} has a value {value}"))
def sensor_has_value_t(context, sensor, value):
    """
    When we receive a fact that the sensor has a value that
    evaluates the next expression...
    """
    sensor = sensor.replace(' ', '_')

    # pylint:disable=exec-used, unused-argument

    def test(val):
        """ test """
        exec("result=val {}".format(value))
        return locals()["result"]
    context.rules.append(SensorFact(name=sensor, value=P(test)))


@then(_("set {sensor} to {value}"))
def set_sensor_value(context, sensor, value):
    """
    Set a sensor to a specific value.
    """
    sensor = Sensor.get(name=sensor.replace(' ', '_'))

    def _set_sensor_value(engine):
        sensor.value = value
        sensor.save()
        sensor.remote_update()

    rules = context.rules.copy()
    context.rules.clear()
    context.final_rules.append(Rule(AND(*rules))(_set_sensor_value))


@when(_("I receive a voice command"))
def voice_command(context):
    """ Dummy step for voice commands """
    pass


class VinistoKE(KnowledgeEngine):
    """
    Custom KnowledgeEngine
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def receive(self, sensors):
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
        for key, a in sensors.items():
            self.retract_matching(SensorFact(name=key))
        self.declare(
            *(SensorFact(name=k, value=v) for k, v in sensors.items()))
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
            parse_feature(data.strip(), None, None).run(runner)
            if runner.undefined_steps:
                raise Exception("Undefined {}".format(runner.undefined_steps))
            yield from context.final_rules

"""
Vinisto Knowledge Engine.
"""

# pylint: disable=no-name-in-module

import string
from copy import deepcopy
from gettext import gettext
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
    # pylint: disable=missing-docstring
    pass


@given(gettext("I have a sensor {name}"))
def add_sensor(_, name):
    """ Add a sensor to db """
    Sensor.get_or_create(name=name, type="sensor")


@given(gettext("I have an infrarred remote {remote} with a button {button}"))
def add_reactor(context, remote, button):
    """
    Add a reactor-type sensor
    I have an infrarred remote {remote} with a button {button}
    """
    try:
        sensor, _ = Sensor.get_or_create(name="{}{}".format(remote, button))
        sensor.type = "button"
        sensor.path = 'lirc/set/{}/{}'.format(remote, button)
        sensor.save()
    except Exception as excp:
        context.exceptions.append(excp)


@given(gettext("I have a {type_} from {toplevel} on {room} "
               "controlling {what}"))
def add_nonreactor(type_, toplevel, room, what):
    """ Add a not-reactive sensor """
    if type_ in Sensor.update_types:
        Sensor.get_or_create(name="{}{}{}{}".format(
                                type_, toplevel, room, what),
                             type=type_,
                             path="{}/set/{}{}".format())
    else:
        Sensor.get_or_create(name="{}{}{}".format(
                                type_, toplevel, room, what),
                             type=type_,
                             path="{}/status/{}{}".format())


@when(gettext("sensor {sensor} has value {value}"))
def sensor_has_value(context, sensor, value):
    """ When we receive a fact that the sensor has a specific value """
    sensor = sensor.replace(' ', '_')
    context.rules.append(SensorFact(name=sensor, value=L(value)))


@when(gettext("sensor {sensor} has a value {value}"))
def sensor_has_value_t(context, sensor, value):
    """
    When we receive a fact that the sensor has a value that
    evaluates the next expression...
    """
    # pylint:disable=exec-used, unused-argument

    def test(val):
        """ test """
        if val and val.isnumeric():
            val = float(val)
        exec("result=val {}".format(value))
        return locals()["result"]
    context.rules.append(SensorFact(name=sensor, value=P(test)))


@when(gettext("sensor {sensor} is off"))
def sensor_is_off(context, sensor, value):
    """
    Sensor is off
    """
    # pylint:disable=exec-used, unused-argument

    def test(val):
        """ test """
        exec("result=val {}".format(value))
        return locals()["result"]
    context.rules.append(SensorFact(name=sensor, value=P(test)))


@then(gettext("set {sensor} to {value}"))
@then(gettext("turn {sensor} {state}"))
def set_sensor_value(context, sensor, value=False, state=False):
    """
    Set a sensor to a specific value.
    """
    if state:
        value = {"on": 1, "off": 0}.get(state)
    sensor = Sensor.get(name=sensor)

    def _set_sensor_value(_):
        sensor.value = value
        sensor.save()
        sensor.remote_update()

    rules = context.rules.copy()
    context.rules.clear()
    context.final_rules.append(Rule(AND(*rules))(_set_sensor_value))


@when(gettext("I receive a voice command"))
def voice_command(_):
    """ Dummy step for voice commands """
    pass


class VinistoKE(KnowledgeEngine):
    """
    Custom KnowledgeEngine
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def receive(self, *args):
        """
        We have received changes in sensors.
        Reset and re-declare all facts.
        TODO: retract_matching isn't working as expected and I dont have time
              to update to pyknow 1.0.0 right now, that's why this reads
              everything again. Sorry.
        """
        sens = Sensor.select()
        self.reset()
        self.declare(*(SensorFact(name=k.name, value=k.value) for k in sens))
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
            context.exceptions = []
            try:
                parse_feature(data.strip(), None, None).run(runner)
                if runner.undefined_steps:
                    raise Exception("Undefined {}".format(
                        runner.undefined_steps))
                print(context.exceptions)
                if context.exceptions:
                    raise Exception(context.exceptions)
                yield from context.final_rules
                # pylint: disable=bare-except
                # TODO: Handle exceptions
            except Exception as err:
                print(err)

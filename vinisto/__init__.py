"""
Vinisto
"""

from gettext import gettext as _
import glob
import json
import random
import string

import paho.mqtt.client as mqtt

from behave import when, then
from behave.configuration import Configuration
from behave.parser import parse_file
from behave.runner import Runner, Context

from pyknow import KnowledgeEngine, Rule, AND, Fact, L, P


class Sensor(Fact):
    """ Sensor fact """
    # pylint: disable=too-few-public-methods
    pass


@when(_("sensor {sensor} has value {value}"))
def sensor_has_value(context, sensor, value):
    """ When we receive a fact that the sensor has a specific value """
    sensor = sensor.replace(' ', '_')
    context.rules.append(Sensor(name=sensor, value=L(value)))


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
    context.rules.append(Sensor(name=sensor, value=P(test)))


@then(_("set {sensor} to {value}"))
def set_sensor_value(context, sensor, value):
    """ Set a sensor to a specific value in mqtt """
    sensor = sensor.replace(' ', '_')

    def _set_sensor_value(engine):
        engine.mqtt.send(context.mqtt_template.format(sensor), value)

    rules = context.rules.copy()
    context.rules.clear()
    context.final_rules.append(Rule(AND(*rules))(_set_sensor_value))


def get_rules(features_dir):
    """ Execute gherkins and return rules """

    config = Configuration()
    config.verbose = True
    runner = Runner(config)

    for filename in glob.glob(features_dir):
        context = Context(runner)
        context.rules = []
        context.final_rules = []
        runner.context = context
        parse_file(filename).run(runner)
        if runner.undefined_steps:
            raise Exception("Undefined {}".format(runner.undefined_steps))
        yield from context.final_rules


def get_knowledge_engine(features_dir):
    """
    Get a knowledge engine built upon a features directory
    """

    def _random_name():
        return ''.join(random.choices(string.ascii_uppercase, 10))

    rules = get_rules(features_dir)
    engine_cls = type(
        "Engine", (KnowledgeEngine,), {_random_name(): rule for rule in rules})
    engine = engine_cls()
    engine.reset()
    return engine


def on_message(client, _, msg):
    """
    Each new mqtt message received, we run the KnowledgeEngine with
    updated data.
    """
    msg = json.loads(msg.payload.decode('utf-8'))

    # Retract previous values of the same sensor.
    for k, _ in msg.items():
        client.engine.retract_matching(Sensor(name=k))

    # Declare new ones
    # This is probably a bad idea, since already-declared
    # things will trigger changes on each message.

    # Wich means... don't touch things manually while using vinisto.
    # And have all your actions have an state (for example, use "turn on"
    # instead of "toggle").

    # This is kind of a problem since that means I can't turn the tv with
    # this method, unless I make some kind of internal state for
    # stateless triggers...
    client.engine.declare(*(Sensor(name=k, value=v) for k, v in msg.items()))
    client.engine.run()


def main(mqtt_connect_data, mqtt_subscription_path, features_dir):
    """
    Connect the mqtt server
    """

    client = mqtt.Client("automation")
    client.engine = get_knowledge_engine(features_dir)
    client.engine.mqtt = client
    client.on_message = on_message
    client.on_disconnect = lambda c, u, r: c.reconnect()
    client.connect(**mqtt_connect_data)
    client.subscribe(mqtt_subscription_path)
    client.loop_forever()

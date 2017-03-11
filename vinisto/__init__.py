"""
Vinisto
"""

from gettext import gettext as _
import glob
import json
import random
import string

import paho.mqtt.client as mqtt

from behave import given, then
from behave.configuration import Configuration
from behave.parser import parse_file
from behave.runner import Runner, Context

from pyknow.engine import KnowledgeEngine
from pyknow.fact import Fact, L, T
from pyknow.rule import AND


class Sensor(Fact):
    """ Sensor fact """
    # pylint: disable=too-few-public-methods
    pass


@given(_("el sensor {sensor} tenga el valor {value}"))
def sensor_has_value(context, sensor, value):
    """ When we receive a fact that the sensor has a specific value """
    sensor = sensor.replace(' ', '_')
    context.rule.append(Sensor(name=sensor, value=L(value)))


@given(_("el sensor {sensor} tenga un valor {value}"))
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
    context.rule.append(Sensor(name=sensor, value=T(test)))


@then(_("establezco {sensor} a {value}"))
def set_sensor_value(context, sensor, value):
    """ Set a sensor to a specific value in mqtt """
    sensor = sensor.replace(' ', '_')

    def _set_sensor_value(engine):
        engine.mqtt.send(context.mqtt_template.format(sensor), value)
    context.rules = AND(*context.rule)(_set_sensor_value)


def get_rules(features_dir):
    """ Execute gherkins and return rules """

    config = Configuration()
    runner = Runner(config)

    for filename in glob.glob(features_dir):
        parse_file(filename).run(runner)
        # TODO: Use the hooks to reset context between features...
        context = Context(runner)
        runner.context = context
        yield context.rules


def on_message(client, _, msg):
    """
    Each new mqtt message received, we run the KnowledgeEngine
    """
    msg = json.loads(msg.payload.decode('utf-8'))

    # Retract previous values of the same sensor.
    for k, _ in msg.items():
        client.engine.retract_matching(Sensor(name=k))

    # Declare new ones
    client.engine.declare(*(Sensor(name=k, value=v) for k, v in msg.items()))
    client.engine.run()


def main(mqtt_connect_data, mqtt_subscription_path, features_dir):
    """
    Connect the mqtt server
    """

    def _random_name():
        return ''.join(random.choices(string.ascii_uppercase, 10))

    rules = get_rules(features_dir)
    client = mqtt.Client("automation")
    client.engine = type(
        "Engine", (KnowledgeEngine,), {_random_name(): rule for rule in rules})
    client.engine.reset()
    client.on_message = on_message
    client.on_disconnect = lambda c, u, r: c.reconnect()
    client.connect(**mqtt_connect_data)
    client.subscribe(mqtt_subscription_path)
    client.loop_forever()

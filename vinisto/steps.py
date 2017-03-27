"""
Steps
"""
from gettext import gettext as _

# pylint: disable=no-name-in-module
from behave import when, then
from pyknow import Rule, AND, L, P
from vinisto.facts import Sensor


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
    """ Set a sensor to a specific value """
    sensor = sensor.replace(' ', '_')

    def _set_sensor_value(engine):
        engine.emit(sensor, value)

    rules = context.rules.copy()
    context.rules.clear()
    context.final_rules.append(Rule(AND(*rules))(_set_sensor_value))


@when(_("I receive a voice command"))
def voice_command(context):
    """ Dummy step for voice commands """
    pass

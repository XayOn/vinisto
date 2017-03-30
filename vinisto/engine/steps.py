"""
Steps
"""
from gettext import gettext as _

# pylint: disable=no-name-in-module
from behave import when, then, given
from pyknow import Rule, AND, L, P
from vinisto.models import Sensor
from vinisto.engine.facts import SensorFact


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

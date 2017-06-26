""" Vinisto Knowledge Engine.

Runs a KE given a specific set of rules (from a directory)

Usage:
    vinisto_engine --db-host <HOST> --db-port <PORT> --db-db <DB> \
--db-user <USER> --db-password <PASSWORD> --db-table <TABLE> --rules-dir <DIR>

Options:
    --db-db=<DB>             Database
    --db-host <HOST>         Host
    --db-port <PORT>         Port
    --db-user <USER>         User
    --db-password <PASSWORD> Pass
    --db-table <TABLE>       Table
    --rules-dir <DIR>        Rules dir

Examples:
    vinisto_engine --db-host localhost --db-port 28015 --db-db vinisto \
--db-user vinisto --db-password vinisto --db-table vinisto --rules-dir \
~/.vinisto_rules
"""

# pylint: disable=no-name-in-module

from contextlib import suppress
from copy import deepcopy
from functools import partial
from gettext import gettext
from random import choice
import logging
import operator
import glob
import string
import sys
import pathlib

import docopt
import rethinkdb as r

from behave import when, then
from behave.configuration import Configuration
from behave.parser import parse_feature
from behave.runner import Runner, Context
from pyknow import Rule, AND, P, Fact, KnowledgeEngine, watchers


logging.basicConfig(level=logging.DEBUG)
watchers.watch()

OPTIONS = docopt.docopt(__doc__)

CONN = r.connect(OPTIONS["--db-host"], OPTIONS["--db-port"],
                 OPTIONS["--db-db"], OPTIONS["--db-user"],
                 OPTIONS["--db-password"])


def _random_name():
    return ''.join(choice(string.ascii_uppercase) for _ in range(10))


def set_value(name, value):
    """ Set value in rethinkdb sensors database """
    r.table(OPTIONS['--db-table']).insert({name: name, value: value},
                                          {"conflict": "update"}).run(CONN)


class SensorFact(Fact):
    # pylint: disable=missing-docstring
    pass


@when(gettext("It's {sensor}"))
@when(gettext("It's {value} {sensor}"))
@when(gettext("sensor {sensor} is {value}"))
@when(gettext("sensor {sensor} has a value {oper} {value}"))
def sensor_has_value_t(context, sensor, oper, value):
    """ Add rule that matches upon sensor changes """
    ops = {'!=': operator.ne, '>=': operator.ge, '>': operator.gt,
           '<': operator.lt, '<=': operator.le, '==': operator.eqt}

    named = {"less than": operator.lt, "greater than": operator.gt,
             "not equal": operator.ne, "not": operator.ne,
             "equal": operator.eq, "less or equal than": operator.le,
             "greater or equal than": operator.gte}

    opera = ops.get(oper, getattr(operator, oper,
                    getattr(named, oper, operator.eq)))
    context.rules.append(SensorFact(name=sensor.replace(' ', '_'),
                         value=P(lambda x: opera(float(x), value))))


@then(gettext("set {sensor} to {value}"))
@then(gettext("turn {sensor} {state}"))
def set_sensor_value(context, sensor, value=False, state=False):
    """ Set a sensor to a specific value.  """
    if state:
        value = {"on": 1, "off": 0}.get(state)

    rules = context.rules.copy()
    context.rules.clear()
    context.final_rules.append(Rule(AND(*rules))(partial(
        set_value, sensor=sensor.replace(' ', '_'), value=value)))


class VinistoEngine:
    """ Vinisto Knowledge Engine class """
    # pylint: disable=too-few-public-methods

    def __new__(cls, **kwargs):
        vals = {_random_name(): rule for rule in cls.get(**kwargs)}
        vals["__name__"] = "KERule"
        engine_cls = type("Engine", (KnowledgeEngine,), vals)
        engine = engine_cls()
        engine.reset()
        return engine

    def get(features_list, base_context):
        """ Execute gherkins and return rules """
        oldsysargv = sys.argv.copy()
        sys.argv = [sys.argv[0]]
        runner = Runner(Configuration())

        for data in features_list:
            context_copy = deepcopy(base_context)
            context = Context(runner)
            for key, value in context_copy.items():
                setattr(context, key, value)
            runner.context = context
            context.exceptions = []
            context.messages = []

            with suppress(Exception):
                parse_feature(data.strip(), None, None).run(runner)
                if context.exceptions or runner.undefined_steps:
                    logging.debug(context.exceptions, runner.undefined_steps)
                yield from context.final_rules

        sys.argv = oldsysargv


def run():
    """ Engine execution entry point """
    rules = [open(f).read() for f in glob.glob(
        pathlib.Path(OPTIONS['--rules-dir']) / '*.feature')]
    engine = VinistoEngine(rules)
    engine.reset()
    engine.declare(*(SensorFact(**k) for k in r.table(OPTIONS['--db-table'])))
    engine.run()

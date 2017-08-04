# noqa: D301
"""Vinisto Knowledge Engine.

Runs a KE given a specific set of rules (from a directory)

Usage:
    vinisto_engine --dbhost <HOST> --dbport <PORT> --dbdb <DB> \
--dbuser <USER> --dbpassword <PASSWORD> --dbtable <TABLE> --rulesdir <DIR>

Options:
    --dbdb=<DB>             Database
    --dbhost <HOST>         Host
    --dbport <PORT>         Port
    --dbuser <USER>         User
    --dbpassword <PASSWORD> Pass
    --dbtable <TABLE>       Table
    --rulesdir <DIR>        Rules dir

Examples:
    vinisto_engine --dbhost localhost --dbport 28015 --dbdb vinisto \
--dbuser vinisto --dbpassword vinisto --dbtable vinisto --rulesdir \
~/.vinisto_rules

"""
# pylint: disable=no-name-in-module

from contextlib import suppress, contextmanager
from copy import deepcopy
from functools import partial
from gettext import gettext
from random import choice
import logging
import operator
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


class SensorFact(Fact):
    """Represents a current sensor state."""

    # pylint: disable=missing-docstring
    pass


@contextmanager
def empty_argv():
    """Behave runner directly uses sys.argv (...). Override it temporarily.

    This context manager sets sys.argv to just the first argument while inside.
    """
    oldsysargv = sys.argv.copy()
    sys.argv = [sys.argv[0]]
    yield
    sys.argv = oldsysargv


@contextmanager
def local_context(base_context, runner, result):
    """Context manager providing a local context on behave.

    Each behave steps will have a local context, reset with
    this fake context manager.
    """
    context_copy = deepcopy(base_context)
    context = Context(runner)

    for key, value in context_copy.items():
        setattr(context, key, value)

    context.exceptions = []
    context.messages = []
    context.result = result
    runner.context = context
    yield


def random_name() -> str:
    """Return a random ascii uppercase name (len 10)."""
    return ''.join(choice(string.ascii_uppercase) for _ in range(10))


def to_operator(from_what: str) -> callable:
    """Given a textual operator return its ``operator`` equivalent.

    Arguments:

        string: String representing the textual operator meaning,
                either in the form "less than", "not equal"... or
                "!=", ">="...

    Returns: ``operator``

    """
    ops = {'!=': operator.ne, '>=': operator.ge, '>': operator.gt,
           '<': operator.lt, '<=': operator.le, '==': operator.eq}

    named = {"less than": operator.lt, "greater than": operator.gt,
             "not equal": operator.ne, "not": operator.ne,
             "equal": operator.eq, "less or equal than": operator.le,
             "greater or equal than": operator.ge}

    return ops.get(from_what, named.get(from_what, operator.eq))


def from_state(state: str) -> int:
    """Given an state (on|off|int), return always an int.

    Arguments:

        string: on|off|str(int)

    """
    return int({"on": "1", "off": "0"}.get(state, state))


@when(gettext("It's {sensor}"))
@when(gettext("It's {value} {sensor}"))
@when(gettext("sensor {sensor} is {value}"))
@when(gettext("sensor {sensor} has a value {oper} {value}"))
def sensor_has_value_t(context: dict, sensor: str, oper: str,
                       value: str) -> None:
    """Add rule that matches upon sensor changes."""
    sensor = sensor.replace(' ', '_')
    context.rules.append(SensorFact(
        name=sensor, value=P(partial(to_operator(oper), value))))


@then(gettext("set {sensor} to {value}"))
@then(gettext("turn {sensor} {value}"))
def set_sensor_value(context: dict, sensor: str, value: bool = False) -> None:
    """Set a sensor to a specific value."""
    rules = context.rules.copy()
    context.rules.clear()

    context.final_rules.append(Rule(AND(*rules))(context.results.__setitem__(
        sensor.replace(' ', '_'), from_state(value))))


class VinistoEngine:
    """Vinisto Knowledge Engine class."""

    # pylint: disable=too-few-public-methods

    def __new__(cls, **kwargs):
        """Create a new derived engine class with dynamic rules."""
        result = {}
        vals = cls.get(result, **kwargs)
        vals = {random_name(): rule for rule in vals}
        vals["__name__"] = "KERule"
        vals['sensors'] = result
        engine_cls = type("Engine", (KnowledgeEngine,), vals)
        engine = engine_cls()
        engine.reset()
        return engine

    @staticmethod
    def get(result, features_list, base_context):
        """Execute gherkins and return rules."""
        with empty_argv():
            runner = Runner(Configuration())
            for data in features_list:
                with local_context(base_context, runner, result) as context:
                    with suppress(Exception):
                        parse_feature(data.strip(), None, None).run(runner)
                    logging.debug(context.exceptions, runner.undefined_steps)
                yield from context.final_rules


def run():
    """Engine execution entry point."""
    options = docopt.docopt(__doc__)

    conn = r.connect(options["--dbhost"], options["--dbport"],
                     options["--dbdb"], options["--dbuser"],
                     options["--dbpassword"])

    rules = (f.read_text() for f in pathlib.Path(
        options['--rulesdir']).glob('*.feature'))

    def set_value(name, value):
        """Set value in rethinkdb sensors database."""
        r.table(options['--dbtable']).insert({name: name, value: value},
                                             {"conflict": "update"}).run(conn)

    engine = VinistoEngine(features_list=rules,
                           base_context={'set_value': set_value})

    # pylint: disable=no-member
    engine.reset()
    engine.declare(*(SensorFact(**k) for k in r.table(options['--dbtable'])))
    engine.run()

    for key, value in engine.result:
        r.table(options['--dbtable']).set(key, value)

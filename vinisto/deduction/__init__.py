# noqa: D301
# docopt requires strings to be literals and examples to be on the
# same line, so we need to override D301 error (backslash on not r'')
"""Vinisto Knowledge Engine.

Runs a KE given a specific set of rules (from a directory)

Usage:
    vinisto_engine --dbhost <HOST> --dbport <PORT> --db <DB> \
--dbuser <USER> --dbpassword <PASSWORD> --dbtable <TABLE> --rulesdir <DIR>

Options:
    --db=<DB>             Database
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

from contextlib import contextmanager
from copy import deepcopy
from functools import partial
from gettext import gettext
from random import choice
import logging
import operator
import string
import sys

import docopt

from behave import when, then
from behave.configuration import Configuration
from behave.parser import parse_feature
from behave.runner import Runner, Context
from pyknow import Rule, AND, P, Fact, KnowledgeEngine, watchers

from . import connectors


logging.basicConfig(level=logging.DEBUG)
watchers.watch()


class SensorFact(Fact):
    """Represents a current sensor state."""


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
def local_context(base_context, runner):
    """Context manager providing a local context on behave.

    Each behave steps will have a local context, reset with
    this fake context manager.
    """
    context_copy = deepcopy(base_context)
    context = Context(runner)

    for key, value in context_copy.items():
        setattr(context, key, value)

    runner.context = context
    yield context
    runner.context = None


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
def get_sensor_value(context: dict, sensor: str, oper: str, val: str) -> None:
    """Add rule that matches upon sensor changes."""
    assert False
    context.rules.append(SensorFact(
        name=sensor.replace(' ', '_'),
        value=P(partial(to_operator(oper), val))))


@then(gettext("set {sensor} to {value}"))
@then(gettext("turn {sensor} {value}"))
def set_sensor_value(context: dict, sensor: str, value: bool = False) -> None:
    """Set a sensor to a specific value."""
    assert False
    rules = context.rules.copy()
    context.rules.clear()

    context.final_rules.append(Rule(AND(*rules))(
        lambda engine: engine.results.__setitem__(
            sensor.replace(' ', '_'), from_state(value))))


class DeductionEngine:
    """Base deduction engine.

    Exposes a run() method that:
    - Creates a knowledge engine based on provided features from the connector
    - Executes given KE
    - Calls connector output method with results from the KE
    """

    def __init__(self, connector):
        """Start with connector."""
        self.connector = connector

    @staticmethod
    def get_engine(rules):
        """Get a composed pyknow KE based on a set of rules.

        get_engine(FeatureParser.get_rules_from(result, rules, context)).
        """
        engine = type("Engine", (KnowledgeEngine,),
                      {random_name(): rule for rule in rules})()
        engine.results = {}
        engine.reset()
        return engine

    @staticmethod
    def get_rules_from(features_list):
        """Execute gherkins and return rules."""
        base_context = {'final_rules': []}
        runner = Runner(Configuration())

        with empty_argv():
            for data in features_list:
                with local_context(base_context, runner) as context:
                    parse_feature(data.strip(), None, None).run(runner)
                    yield from context.final_rules

    def run(self):
        """Extract CLI options and runs engine."""
        # pylint: disable=no-member
        engine = self.get_engine(self.connector.features())
        engine.declare(*(SensorFact(**k) for k in self.connector.input()))
        engine.run()
        return self.connector.output(engine.results)


def run():
    """Execute DeductionEngine with given connector and options."""
    args = docopt.docopt(__doc__)
    connector = getattr(connectors, args.pop('--connector'))(args)
    return DeductionEngine(connector).run()

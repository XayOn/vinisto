""" Deduction engine unit tests """

# pylint: disable=invalid-name, missing-docstring

import operator
import pytest


def test_can_parse_basic_feature():
    """ Test that parsing a simple equality feature produces a correct
        pyknow rule with a single equality fact """
    from vinisto.deduction import DeductionEngine, SensorFact

    feature = """Feature: Test features parser
Scenario: Test features parser
   When sensor sensor has a value equal to 10
   Then set sensor_2 to 10"""
    rules = list(DeductionEngine.get_rules_from([feature]))
    engine = DeductionEngine.get_engine(rules)
    fact = engine.get_rules()[0][0]
    assert fact == SensorFact(sensor=10)


def test_empty_argv():
    from vinisto.deduction import empty_argv
    import sys
    sys.argv = ["asdf", "bar", "foo"]
    with empty_argv():
        assert sys.argv == ['asdf']
    assert sys.argv == ["asdf", "bar", "foo"]


def test_local_context():
    from vinisto.deduction import local_context
    from unittest.mock import patch, MagicMock

    fake_runner = MagicMock()
    base_context = {'baz': 'stuff'}

    with patch('vinisto.deduction.Context') as fake_context:
        with local_context(base_context, fake_runner):
            assert fake_runner.context == fake_context()


@pytest.mark.parametrize('origin, normalized', (
    ('!=', operator.ne),
    ('>=', operator.ge),
    ('>', operator.gt),
    ('<', operator.lt),
    ('<=', operator.le),
    ('==', operator.eq),
    ("less than", operator.lt),
    ("greater than", operator.gt),
    ("not equal", operator.ne),
    ("not", operator.ne),
    ("equal", operator.eq),
    ("less or equal than", operator.le),
    ("greater or equal than", operator.ge)))
def test_to_operator(origin, normalized):
    from vinisto.deduction import to_operator
    assert to_operator(origin) == normalized


@pytest.mark.parametrize('state, result', (('on', 1), ('off', 0), ('9', 9)))
def test_from_state(state, result):
    from vinisto.deduction import from_state
    assert from_state(state) == result

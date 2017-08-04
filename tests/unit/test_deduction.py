""" Deduction engine unit tests """

# pylint: disable=invalid-name, missing-docstring

import operator
import pytest


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
    result = {"foo": "bar"}
    base_context = {'baz': 'stuff'}

    with patch('vinisto.deduction.Context') as fake_context:
        with local_context(base_context, fake_runner, result):
            # TODO: Test deepcopy
            assert fake_runner.context == fake_context()
            assert fake_runner.context.messages == []
            assert fake_runner.context.result is result
            # assert fake_runner.context['baz'] == 'stuff'


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


def test_vinistoengine_creation():
    from vinisto.deduction import VinistoEngine
    from unittest.mock import patch

    get_method = 'vinisto.deduction.VinistoEngine.get'
    with patch(get_method, side_effect=({'foo': 'bar'},)):
        # pylint: disable=no-member
        engine = VinistoEngine()
        assert engine.__name__ == "KERule"
        assert engine.sensors == {}
        # assert engine.foo == "bar"


# TODO: test behave functions
# TODO: Test VinistoEngine.get

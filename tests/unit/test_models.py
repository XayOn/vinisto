import pytest


def test_feature_has_all_attrs():
    from vinisto.models import FeatureModel
    assert hasattr(FeatureModel, "base")
    assert hasattr(FeatureModel, "variables")


def test_sensor_has_all_attrs():
    from vinisto.models import SensorModel

    assert hasattr(SensorModel, "name")
    assert hasattr(SensorModel, "value")
    assert hasattr(SensorModel, "type")
    assert hasattr(SensorModel, "http_verb")
    assert hasattr(SensorModel, "url_template")
    assert hasattr(SensorModel, "data_template")
    assert hasattr(SensorModel, "update_types")


@pytest.mark.parametrize("method", ("get", "post"))
def test_remote_update(method):
    from unittest.mock import patch
    with patch("requests.{}".format(method)) as mock:
        from vinisto.models import SensorModel
        sensor, _ = SensorModel.get_or_create(
            type="button",
            name="test", value="1", http_verb=method,
            url_template="http://localhost/{name}/{value}",
            data_template='{{"name": "{name}", "value": "{value}"}}')

        sensor.remote_update()
        mock.assert_called_with(
            "http://localhost/test/1",
            data={"name": "test", "value": "1"})


def test_get_engine_returns_engine():
    import json
    from pyknow import KnowledgeEngine
    from vinisto.models import FeatureModel
    from vinisto.abstract import AbstractEmitter

    class Emitter(metaclass=AbstractEmitter):
        def emit(self, *args):
            pass

    base = """
    Feature: Foo
    Scenario: If there is cold, turn the heat on
              When I receive {command}
              Then set sensor a to {value}
    """
    variables = json.dumps({"command": "a voice command", "value": "8"})
    FeatureModel.get_or_create(base=base, variables=variables)
    assert isinstance(
        FeatureModel.get_engine(FeatureModel.select(), Emitter()),
        KnowledgeEngine)

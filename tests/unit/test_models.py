import pytest


def test_feature_has_all_attrs():
    from vinisto.models import Feature
    assert hasattr(Feature, "text")


def test_sensor_has_all_attrs():
    from vinisto.models import Sensor

    assert hasattr(Sensor, "name")
    assert hasattr(Sensor, "value")
    assert hasattr(Sensor, "type")
    assert hasattr(Sensor, "http_verb")
    assert hasattr(Sensor, "url_template")
    assert hasattr(Sensor, "data_template")
    assert hasattr(Sensor, "update_types")


@pytest.mark.parametrize("method", ("get", "post"))
def test_remote_update(method):
    from unittest.mock import patch
    with patch("requests.{}".format(method)) as mock:
        from vinisto.models import Sensor
        sensor, _ = Sensor.get_or_create(
            type="button",
            name="test", value="1", http_verb=method,
            url_template="http://localhost/{name}/{value}",
            data_template='{{"name": "{name}", "value": "{value}"}}')

        sensor.remote_update()
        mock.assert_called_with(
            "http://localhost/test/1",
            data={"name": "test", "value": "1"})


def test_get_engine_returns_engine():
    from pyknow import KnowledgeEngine
    from vinisto.models import Feature

    text = """
    Feature: Foo
    Scenario: If there is cold, turn the heat on
              Given I have a sensor a
              When I receive a voice command
              Then set a to 8
    """
    Feature.get_or_create(text=text)
    assert isinstance(Feature.get_engine(Feature.select()), KnowledgeEngine)

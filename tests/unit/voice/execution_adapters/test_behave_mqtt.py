def test_BehaveMQTT_executes_phrase(config):
    import vinisto.voice.execution_adapters.behave_mqtt as behave_mqtt
    from unittest.mock import patch
    behave_mqtt.BehaveMQTT().execute_from_phrase("set sensor home to 1")
    mock.assert_called_with(behave_mqtt.BehaveMQTT.template.format(
        "set sensor home to 1"))

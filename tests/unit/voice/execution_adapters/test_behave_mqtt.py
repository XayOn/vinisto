def test_BehaveMQTT_executes_phrase(config):
    import vinisto.voice.execution_adapters.behave_mqtt as behave_mqtt
    from unittest.mock import patch

    with patch("vinisto.main", return_value=True) as mock:
        behave_mqtt.BehaveMQTT(config).execute_from_phrase("foo")
        mock.assert_called_with(behave_mqtt.BEHAVE_MQTT_TEMPLATE.format("foo"))

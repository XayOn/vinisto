def test_BehaveMQTT_executes_phrase(config):
    import vinisto.voice.execution_adapters.behave_mqtt as behave_mqtt
    from unittest.mock import patch

    with patch("vinisto.main", return_value=True) as mock:
        with patch("vinisto.config", return_value=config):
            behave_mqtt.BehaveMQTT().execute_from_phrase("foo")
            mock.assert_called_with(behave_mqtt.BehaveMQTT.template.format(
                "foo"))

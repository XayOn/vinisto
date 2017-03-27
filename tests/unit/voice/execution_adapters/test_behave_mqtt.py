def test_BehaveMQTT_executes_phrase(config):
    from unittest.mock import MagicMock
    import vinisto.voice.execution_adapters.behave_mqtt as behave_mqtt
    from vinisto.abstract import AbstractEmitter
    emitter = MagicMock(spec=AbstractEmitter)
    behave_mqtt.BehaveMQTT(emitter=emitter).execute_from_phrase(
        "set air conditioner to 1")
    emitter.emit.assert_called_with("air_conditioner", "1")

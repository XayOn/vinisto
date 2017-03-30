def test_speechrecognition_mic_id(config):
    from unittest.mock import patch, MagicMock
    with patch("vinisto.services.connectors.voice.config", return_value=config) as cmock:
        import vinisto.services.connectors.voice as sr
        with patch("vinisto.services.connectors.voice.speech") as mock:
            cmock.items = MagicMock(
                return_value={"microphone_name": "basic_microphone"})
            mock.Microphone.list_microphone_names = MagicMock(return_value=[
                "basic_microphone", "nope_microphone"])

            recog = sr.SpeechRecognition()
            mock.Microphone.list_microphone_names.assert_called_once_with()
            mic_id = recog.mic_id
            assert mic_id == 0


def test_speechrecognition_mic_id_defaults_as_pulse(config):
    from unittest.mock import patch, MagicMock

    with patch("vinisto.services.connectors.voice.config", return_value=config) as cmock:
        import vinisto.services.connectors.voice as sr
        with patch("vinisto.services.connectors.voice.speech") as mock:

            mock.Microphone.list_microphone_names = MagicMock(return_value=[
                "basic_microphone", "pulse"])

            recog = sr.SpeechRecognition()
            mock.Microphone.list_microphone_names.assert_called_once_with()
            mic_id = recog.mic_id
            assert mic_id == 1

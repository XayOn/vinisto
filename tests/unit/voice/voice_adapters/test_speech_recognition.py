def test_speechrecognition_mic_id(config):
    import vinisto.services.voice.voice_adapters.vinisto_speech_recognition as sr
    from unittest.mock import patch, MagicMock

    with patch("vinisto.services.voice.voice_adapters."
               "vinisto_speech_recognition.config",
               return_value=config) as cmock:
        with patch("vinisto.services.voice.voice_adapters.vinisto_speech_"
                   "recognition.speech") as mock:
            cmock.items = MagicMock(
                return_value={"microphone_name": "basic_microphone"})
            mock.Microphone.list_microphone_names = MagicMock(return_value=[
                "basic_microphone", "nope_microphone"])

            recog = sr.SpeechRecognition()
            mock.Microphone.list_microphone_names.assert_called_once_with()
            mic_id = recog.mic_id
            assert mic_id == 0


def test_speechrecognition_mic_id_defaults_as_pulse(config):
    import vinisto.services.voice.voice_adapters.vinisto_speech_recognition as sr
    from unittest.mock import patch, MagicMock

    with patch("vinisto.services.voice.voice_adapters."
               "vinisto_speech_recognition.config",
               return_value=config) as cmock:
        with patch("vinisto.services.voice.voice_adapters.vinisto_speech_"
                   "recognition.speech") as mock:
            cmock.items = MagicMock(
                return_value={})
            mock.Microphone.list_microphone_names = MagicMock(return_value=[
                "basic_microphone", "pulse"])

            recog = sr.SpeechRecognition()
            mock.Microphone.list_microphone_names.assert_called_once_with()
            mic_id = recog.mic_id
            assert mic_id == 1

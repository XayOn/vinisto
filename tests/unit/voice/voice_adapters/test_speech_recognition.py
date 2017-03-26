def test_speechrecognition_mic_id(config):
    import vinisto.voice.voice_adapters.vinisto_speech_recognition as sr
    from unittest.mock import patch, MagicMock
    with patch("vinisto.voice.voice_adapters.vinisto_speech_"
               "recognition.speech") as mock:
        recog = sr(config)
        mic_id = recog.mic_id
        mock.Microphone.list_microphone_names = MagicMock(return_value=[
            "basic_microphone", "nope_microphone"])
        mock.microphones.assert_called_once()
        mock.Microphone.list_microphone_names.assert_called_once()
        assert mic_id == 0

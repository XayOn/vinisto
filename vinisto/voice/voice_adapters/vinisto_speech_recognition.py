"""
Speech recognition
"""

from functools import lru_cache
import speech_recognition as speech
from vinisto.voice.abstract import VoiceAdapter


class SpeechRecognition(metaclass=VoiceAdapter):
    """
    VoiceAdapter using SpeechRecognition.
    This reads the configuration file to complete the
    required parameters as documented in speech_recognition API

    github.com/Uberi/speech_recognition/blob/master
    /reference/library-reference.rst

    """

    def __init__(self, config):
        self.recognizer = speech.Recognizer()
        speech_config = dict(config.items(speech))
        self.microphone = speech_config.pop("microphone_name", "pulse")
        self.recognition_class = speech_config.pop("recognizer", "pulse")
        self.config = speech_config
        self.source = speech.Microphone(device_index=self.mic_id)

    @lru_cache()
    def mic_id(self):
        """ Return the selected microphone ID """
        all_m = speech.Microphone.list_microphone_names()
        matching = [idx for idx, name in enumerate(all_m)
                    if name == self.microphone]
        return matching.pop()

    @property
    @lru_cache()
    def recognize(self):
        """
        Return recognizer with recognition class
        """
        return getattr(self.recognizer, self.recognition_class)

    def __next__(self):
        """
        Iterate returning text until an exception happens.

        This way, when we cannot understand the voice, we can
        interact with the user
        """
        try:
            with self.source as source:
                return self.recognize(
                    self.recognizer.listen(source), **self.config)
        except Exception:
            raise StopIteration

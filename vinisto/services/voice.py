"""
Vinisto voice module, using different voice and execution adapters
"""

import speech_recognition as speech
from vinisto.services import RestConnector
from vinisto import config
import asyncio


class SpeechRecognition:
    """
    VoiceAdapter using SpeechRecognition.
    This reads the configuration file to complete the
    required parameters as documented in speech_recognition API

    github.com/Uberi/speech_recognition/blob/master
    /reference/library-reference.rst

    """

    def __init__(self):
        self.recognizer = speech.Recognizer()
        speech_config = dict(config.items("speech"))
        self.microphone = speech_config.pop("microphone_name", "pulse")
        self.recognition_class = speech_config.pop("recognizer", "google")
        self.config = speech_config
        self.source = speech.Microphone(device_index=self.mic_id)

    @property
    def microphones(self):
        """ Return a list of available microphones on the system """
        return speech.Microphone.list_microphone_names()

    @property
    def mic_id(self):
        """ Return the selected microphone ID """
        matching = [idx for idx, name in enumerate(self.microphones)
                    if name == self.microphone]
        try:
            return matching.pop()
        except IndexError:
            raise Exception("No microphone matching given id %s, %s"
                            % (self.microphone, self.microphones))

    @property
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


class VinistoVoice:
    """
    Main class
    """
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.voice_adapter = SpeechRecognition()
        self.connector = RestConnector()

    async def run(self):
        """
        Main loop.

        If we actually have a StopIteration from the voice adapter,
        we stop.

        We can only have one voice adapter at a time, but multiple
        executor adapters.

        Be careful, if your executor adapters react to the same
        things, there can be repeated executions.
        """
        async for voice_input in self.voice_adapter:
            self.connector.execute_then(self.template.format(voice_input))


def run():
    voiceadapter = VinistoVoice()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(voiceadapter.run())
    loop.close()

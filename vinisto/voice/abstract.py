"""
Abstract definition for voice modules
"""

import abc


class VoiceAdapter(abc.ABCMeta):
    """
    Main voice adapter base class
    """

    @abc.abstractmethod
    def __init__(cls):
        super().__init__()

    def __iter__(cls):
        return cls

    @abc.abstractmethod
    def __next__(cls):
        data = cls.get_voice_input()

        if data:
            return data
        else:
            raise StopAsyncIteration


class ExecutorAdapter(abc.ABCMeta):
    """
    Execution adaptor base class
    """

    @abc.abstractmethod
    def execute_from_phrase(cls, phrase):
        """
        Given a phrase, execute what the adapter has associated for it.
        """
        pass

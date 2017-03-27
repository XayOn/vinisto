"""
Vinisto voice module, using different voice and execution adapters
"""

from .abstract import VoiceAdapter, ExecutorAdapter


class VinistoVoice:
    """
    Main class
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, voice_adapter, executor_adapters):
        assert isinstance(voice_adapter, VoiceAdapter)
        assert all(isinstance(executor, ExecutorAdapter)
                   for executor in executor_adapters)
        self.voice_adapter = voice_adapter
        self.executor_adapters = executor_adapters

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
            for executor_adapter in self.executor_adapters:
                executor_adapter.execute_from_phrase(voice_input)

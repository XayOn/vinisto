""" Behave adapter. Uses the same logic as main vinisto module """

from gettext import gettext as _
from vinisto.voice.abstract import ExecutorAdapter
import vinisto


class Behave(metaclass=ExecutorAdapter):
    """
    Execution adaptor base class
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, emitter):
        self.emitter = emitter

    template = _("""Feature: Voice recognition
      Scenario: I received a voice command
           When I receive a voice command
           Then {}""")

    def execute_from_phrase(self, phrase):
        """
        Given a phrase, execute what the adapter has associated for it.
        """
        feature = self.template.format(phrase)
        engine = vinisto.engine.VinistoEngine(
            emitter=self.emitter,
            features_list=[feature],
            base_context={"rules": [], "final_rules": []})
        return engine.run()
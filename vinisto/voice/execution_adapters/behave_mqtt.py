"""
Behave+MQTT adapter. Uses the same logic as main vinisto module
to send data to an MQTT server using voice commands.

"""

from gettext import gettext as _
from vinisto.voice.abstract import ExecutorAdapter
import vinisto


class BehaveMQTT(metaclass=ExecutorAdapter):
    """
    Execution adaptor base class
    """
    # pylint: disable=too-few-public-methods

    template = _("""Feature: Voice recognition
      Scenario: I received a voice command
           Then {}""")

    def execute_from_phrase(self, phrase):
        """
        Given a phrase, execute what the adapter has associated for it.
        """
        feature = self.template.format(phrase)
        vinisto.main(feature)

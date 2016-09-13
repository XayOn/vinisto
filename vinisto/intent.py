"""
    Intent related
"""

from vinisto.language import Phrase, SinonymPhrase,


class Intent:
    """
        A base intent.
    """
    def __init__(self, phrases):
        assert all((type(phrase) for phrase in phrases))
        self.phrases = phrases

    def __eq__(self, other):
        assert isinstance(other, Phrase)
        if other in self.phrases:
            return True
        elif SyntacticMatchPhrase(other) in self:
            return True
        else:
            return SynonimPhrase(other) in self

    def __iter__(self):
        for i in self.phrases:
            yield i

    def __repr__(self):
        return f'Intent {self.__class__.__name__} with {self.phrases}'

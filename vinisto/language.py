import nltk
import PyDictionary
from py3translate.microsoft import Bing
from nltk.tokenize import word_tokenize
import itertools
import gensim

""" TODO: handle CC and split in multiple phrases the origin frase """

bing = Bing("a", "b")

PYDICT = PyDictionary.PyDictionary()


class SynonimPhrase:
    def __init__(self, phrase):
        def get_synonims(phrase):
            """ Return synonims for a phrase """
            for word, _ in phrase.phrase:
                try:
                    yield list(PYDICT.synonym(word))
                except:
                    yield [word]

        self._phrase = phrase
        sins = itertools.product(*get_synonims(self._phrase))
        types = list(zip(*self._phrase))[-1]
        self.phrases = [Phrase(tuple(zip(sin_, types))) for sin_ in sins]

    def __eq__(self, other):
        if other.language == self.language:
            return self.phrase == other.phrase

        return other.to_lang(self.language) in self.phrases


class SintacticMatchPhrase:
    pass


class Phrase:
    """
        Phrase

        Comparing a phraes with another in a different language
        will trigger a translation module that will translate THE OTHER
        phrase

    """

    def __init__(self, phrase, language="en"):
        self.language = language
        if not isinstance(phrase, tuple):
            self.phrase = nltk.pos_tag(word_tokenize(phrase))
        else:
            self.phrase = phrase

    def __eq__(self, other):
        if other.language == self.language:
            return self.phrase == other.phrase

        return other.to_lang(self.language) == self

    def to_lang(self, lang):
        """
            Translate ourselves to another language
            If our current language is the same as requested, return self.

            .. WARNING: This actually replaces ourself with a new phrase in
            the new language. This might need review.

        """

        def _to_lang(phrase):
            """ Translate to english """
            for word, type_ in phrase:
                yield (bing.translate(word, self.language, lang), type_)

        if self.language == lang:
            return self
        else:
            self = Phrase(tuple(_to_lang(self.phrase)))
            self.language = lang
            return self

    @property
    def c_phrase(self):
        return ' '.join([a[0] for a in self.phrase])

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.c_phrase} - {self.language}'

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk import UnigramTagger
import nltk.corpus
from nltk.stem import WordNetLemmatizer


class Tagger(object):
    def __init__(self, cess_name="cess_esp"):
        """
            Tagger object.
            Allows to specify a cess.
        """
        cess = getattr(nltk.corpus, cess_name)
        self.wnl = WordNetLemmatizer()
        self.ut = UnigramTagger(cess.tagged_sents())

    def pos_tag(self, tokens, lemmatize=False):
        def clean_tag(tag):
            def get_type(tag):
                if tag[1]:
                    return tag[1][0].upper()
                return "X"
            if lemmatize:
                return (self.wnl.lemmatize(tag[0]), get_type(tag))
            return (tag[0], get_type(tag))

        if type(tokens) == str:
            tokens = tokens.split()

        return [clean_tag(a) for a in self.ut.tag(tokens)]

    def get_main_words(self, tokens, lemmatize=True, type_w=False):
        def cond(t):
            if type_w:
                for type_w_ in type_w:
                    if t[1].lower().startswith(type_w_.lower()):
                        return True
                return False
            return True

        return filter(cond, self.pos_tag(tokens, lemmatize=lemmatize))

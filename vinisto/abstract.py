"""
Abstract classes
"""

import abc


class AbstractEmitter(abc.ABCMeta):
    """ Emitter abstract class """

    @abc.abstractmethod
    def emit(cls):
        """ emit """
        pass

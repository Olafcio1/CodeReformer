import pygame
from abc import ABCMeta

class ForceRenderable(metaclass=ABCMeta):
    _forceRerender: bool

    def __init__(self):
        self._forceRerender = False

    def pendingRerender(self) -> bool:
        if self._forceRerender:
            self._forceRerender = False
            return True

        return False

    def forceRender(self) -> None:
        self._forceRerender = True

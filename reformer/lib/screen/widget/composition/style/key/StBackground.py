import pygame

from abc import ABCMeta
from typing import Self, overload

ColorValue = pygame.Color | tuple[int, int, int] | int
OptColor = ColorValue | None

class StBackground(metaclass=ABCMeta):
    _background: OptColor = None

    @overload
    def background(self) -> OptColor:
        ...

    @overload
    def background(self, value: OptColor, /) -> Self:
        ...

    def background(self, *params):
        if len(params) == 0:
            return self._background
        elif len(params) == 1:
            self._background = params[0]
            return self
        else:
            raise Exception("No matching overload")

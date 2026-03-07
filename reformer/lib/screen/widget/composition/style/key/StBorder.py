import pygame

from abc import ABCMeta
from typing import Self, overload

ColorValue = pygame.Color | tuple[int, int, int] | int
OptColor = ColorValue | None

class StBorder(metaclass=ABCMeta):
    _borderTop: OptColor = None
    _borderBottom: OptColor = None

    _borderLeft: OptColor = None
    _borderRight: OptColor = None

    @overload
    def border(self) -> tuple[OptColor, OptColor, OptColor, OptColor]:
        ...

    @overload
    def border(self, value: tuple[OptColor, OptColor, OptColor, OptColor], /) -> Self:
        ...

    def border(self, *params):
        if len(params) == 0:
            return (
                self._borderTop,
                self._borderBottom,
                self._borderLeft,
                self._borderRight
            )
        elif len(params) == 1:
            self._borderTop, \
            self._borderBottom, \
            self._borderLeft, \
            self._borderRight = params[0]

            return self
        else:
            raise Exception("No matching overload")

    def borderTop(self, value: OptColor) -> Self:
        self._borderTop = value
        return self

    def borderBottom(self, value: OptColor) -> Self:
        self._borderBottom = value
        return self

    def borderLeft(self, value: OptColor) -> Self:
        self._borderLeft = value
        return self

    def borderRight(self, value: OptColor) -> Self:
        self._borderRight = value
        return self

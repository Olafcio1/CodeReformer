import pygame

from .Style import Style

from ...Widget import Widget
from ....iwidget.IContainer import IContainer

from typing import Self

class Styleable(IContainer):
    style: Style[Self]

    def __init__(self):
        self.style = Style(self)

    def applyPre(self, surface: pygame.Surface) -> None:
        if self.style._background != None:
            surface.fill(self.style._background, (self.x, self.y, self.width, self.height))

        self.__pad(1)

        if self.style._display == "non-managed":
            pass
        elif self.style._display == "grid":
            prev: Widget|None = None
            x = 0

            for element in self._renderables:
                if isinstance(element, Widget):
                    if prev != None:
                        x += prev.height
                        x += self.style._gapVertical

                    element.x = 0
                    element.y = x

                    prev = element
        elif self.style._display == "flex":
            prev: Widget|None = None
            x = 0

            for element in self._renderables:
                if isinstance(element, Widget):
                    if prev != None:
                        x += prev.width
                        x += self.style._gapHorizontal

                    element.x = x
                    element.y = 0

                    prev = element
        else:
            raise Exception("Invalid 'display' value")

    def applyPost(self, surface: pygame.Surface) -> None:
        self.__pad(-1)

        if self.style._borderTop    != None: surface.fill(self.style._borderTop, (self.x, self.y, self.width, 1))
        if self.style._borderBottom != None: surface.fill(self.style._borderBottom, (self.x, self.y + self.height - 1, self.width, 1))

        if self.style._borderLeft  != None: surface.fill(self.style._borderLeft, (self.x, self.y, 1, self.height))
        if self.style._borderRight != None: surface.fill(self.style._borderRight, (self.x + self.width - 1, self.y, 1, self.height))

    def __pad(self, mul: int) -> None:
        self.x += self.style._paddingLeft * mul
        self.y += self.style._paddingTop * mul

        self.width -= self.style._paddingLeft * mul
        self.width -= self.style._paddingRight * mul

        self.height -= self.style._paddingTop * mul
        self.height -= self.style._paddingBottom * mul

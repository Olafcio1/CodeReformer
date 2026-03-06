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
        self.__pad(1)

        if self.style._display == "non-managed":
            pass
        elif self.style._display == "grid":
            prev: Widget|None = None
            y = 0

            for element in self._renderables:
                if isinstance(element, Widget):
                    if prev != None:
                        y += prev.height
                        y += self.style._gap

                    element.x = 0
                    element.y = y

                    prev = element
        else:
            raise Exception("Invalid 'display' value")

    def applyPost(self, surface: pygame.Surface) -> None:
        self.__pad(-1)

    def __pad(self, mul: int) -> None:
        self.x += self.style._paddingLeft * mul
        self.y += self.style._paddingTop * mul

        self.width -= self.style._paddingLeft * mul
        self.width -= self.style._paddingRight * mul

        self.height -= self.style._paddingTop * mul
        self.height -= self.style._paddingBottom * mul

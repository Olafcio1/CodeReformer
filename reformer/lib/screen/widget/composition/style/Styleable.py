import pygame

from .Style import Style

from ....iwidget.IWidget import IWidget
from ....iwidget.IContainer import IContainer

from typing import Self

class Styleable(IContainer):
    __style: Style[Self]

    @property
    def style(self):
        return self.__style

    def __init__(self):
        self.__style = Style(self)

    ###########
    ## APPLY ##
    ###########

    def applyPre(self, surface: pygame.Surface) -> None:
        if self.style._background != None:
            surface.fill(self.style._background, (self.x, self.y, self.width, self.height))

        if self.style._display == "non-managed":
            pass
        elif self.style._display == "grid":
            prev: IWidget|None = None
            y = self.style._paddingTop

            for element in self._widgets:
                if prev != None:
                    y += prev.height
                    y += self.style._gapVertical

                x = self.style._paddingLeft

                if hasattr(element, 'style'):
                    x += element.style._marginLeft # type: ignore
                    y += element.style._marginTop  # type: ignore

                element.x = x
                element.y = y

                if hasattr(element, 'style'):
                    y += element.style._marginBottom  # type: ignore

                prev = element
        elif self.style._display == "flex":
            prev: IWidget|None = None
            x = self.style._paddingLeft

            for element in self._widgets:
                if prev != None:
                    x += prev.width
                    x += self.style._gapHorizontal

                y = self.style._paddingTop

                if hasattr(element, 'style'):
                    x += element.style._marginLeft # type: ignore
                    y += element.style._marginTop  # type: ignore

                element.x = x
                element.y = y

                if hasattr(element, 'style'):
                    x += element.style._marginRight # type: ignore

                prev = element
        else:
            raise Exception("Invalid 'display' value")

    def applyPost(self, surface: pygame.Surface) -> None:
        if self.style._borderTop    != None: surface.fill(self.style._borderTop, (self.x, self.y, self.width, 1))
        if self.style._borderBottom != None: surface.fill(self.style._borderBottom, (self.x, self.y + self.height - 1, self.width, 1))

        if self.style._borderLeft  != None: surface.fill(self.style._borderLeft, (self.x, self.y, 1, self.height))
        if self.style._borderRight != None: surface.fill(self.style._borderRight, (self.x + self.width - 1, self.y, 1, self.height))

    ##########
    ## SIZE ##
    ##########

    @property
    def innerWidth(self) -> int:
        return self.width - self.style._paddingLeft - self.style._paddingRight

    @property
    def innerHeight(self) -> int:
        return self.height - self.style._paddingTop - self.style._paddingBottom

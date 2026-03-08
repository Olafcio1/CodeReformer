from abc import ABCMeta
from typing import overload

from ...iwidget.IWidget import IWidget

class Hoverable(IWidget, metaclass=ABCMeta):
    __hovered: bool
    __usesHover: bool

    def __init__(self):
        self.__hovered = False
        self.__usesHover = False

    @overload
    def isHovered(self) -> bool:
        ...

    @overload
    def isHovered(self, x: int, y: int, /) -> bool:
        ...

    def isHovered(self, *params) -> bool:
        if len(params) == 0:
            self.__usesHover = True
            return self.__hovered
        elif len(params) == 2:
            x, y = params
            return x >= self.x and y >= self.y and x < self.x + self.width and y < self.y + self.height
        else:
            raise Exception("No matching overload")

    def mouseMoved(self, x: int, y: int) -> None:
        super().mouseMoved(x, y)  # type: ignore
        self.__hovered = self.isHovered(x, y)

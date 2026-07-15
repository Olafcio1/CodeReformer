from ..proxy.StyleProxy import StyleProxy
from ...Backable import Backable, T
from .....iwidget.IHoverable import IHoverable

from abc import ABCMeta
from typing import Generic, TypeVar

S = TypeVar('S', bound=Backable[T])

class AStyleable(Generic[S], metaclass=ABCMeta):
    __style: S
    __style_plain: S
    __style_hover: S

    @property
    def style(self):
        return self.__style

    @property
    def style_plain(self):
        return self.__style_plain

    @property
    def style_hover(self):
        return self.__style_hover

    def __init__(self, Style: type[S]):
        self.__style_plain = Style(self)
        self.__style_hover = Style(self)

        self.__style = StyleProxy(self.__style_plain, self.__callback)

    def __callback(self, name: str) -> S:
        self: IHoverable

        if self.isHovered() and self.__style_hover.isSet(name.removeprefix("_")):
            return self.__style_hover
        else:
            return self.__style_plain

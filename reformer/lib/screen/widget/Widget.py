import pygame

from .Attacher import Attacher
from .Initializable import Initializable

from .builder.WidgetBuilder import WidgetBuilder
from .composition.style.mini.MiniStyleable import MiniStyleable

from .universal.Parented import Parented
from .universal.Represented import Represented
from .universal.Hoverable import Hoverable

from ..iwidget.IWidget import IWidget

from abc import ABCMeta, abstractmethod
from typing import final, Self

class Widget(
        Attacher, Initializable,
        Parented, Represented,
        Hoverable, MiniStyleable,

        IWidget,

        metaclass=ABCMeta
):
    x: int
    y: int

    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        Attacher.__init__(self)
        Parented.__init__(self)
        Hoverable.__init__(self)
        Initializable.__init__(self)
        MiniStyleable.__init__(self)

    #############
    ## GETTERS ##
    #############

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)

    ###############
    ## RENDERING ##
    ###############

    @final
    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        super().applyPre(surface)

        self.renderWidget(surface)
        self._reset()

        super().applyPost(surface)

    @final
    def renderChanged(self, surface: pygame.Surface) -> None:
        super().renderChanged(surface)

    ######################
    ## PENDING RERENDER ##
    ######################

    def pendingRerender(self) -> bool:
        return super().pendingRerender() or self._interacted()

    ##############
    ## ABSTRACT ##
    ##############

    @abstractmethod
    def renderWidget(self, surface: pygame.Surface) -> None:
        ...

    def getText(self) -> str:
        return ""

    #############
    ## BUILDER ##
    #############

    @classmethod
    def Builder(cls) -> WidgetBuilder[Self]:
        return WidgetBuilder(cls)

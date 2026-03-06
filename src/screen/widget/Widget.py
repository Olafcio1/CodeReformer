import pygame

from .Attacher import Attacher
from .Initializable import Initializable

from .builder.WidgetBuilder import WidgetBuilder
from ..iwidget.IWidget import IWidget

from abc import ABCMeta, abstractmethod
from typing import final, Self

class Widget(
        Attacher, Initializable,
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

        super(Attacher, self).__init__()
        super(Initializable, self).__init__()

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
        self.renderWidget(surface)
        self._reset()

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

    #############
    ## BUILDER ##
    #############

    @classmethod
    def Builder(cls) -> WidgetBuilder[Self]:
        return WidgetBuilder(cls)

import pygame
import time

from .Attacher import Attacher
from .Initializable import Initializable

from .builder.WidgetBuilder import WidgetBuilder
from .composition.style.mini.MiniStyleable import MiniStyleable

from .universal.Parented import Parented
from .universal.Represented import Represented
from .universal.Hoverable import Hoverable

from ..iwidget.IWidget import IWidget

from abc import ABCMeta, abstractmethod
from typing import Self, final, overload
from threading import Thread

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

    @overload
    def __init__(self, x: int, y: int, width: int, height: int, /):
        ...

    @overload
    def __init__(self, *, x: int, y: int, width: int, height: int):
        ...

    @overload
    def __init__(self):
        """Initializes a widget on X;Y 0,0 with the full screen size."""
        ...

    def __init__(self, *args, **kwargs):
        if len(args) == 4 and len(kwargs) == 0:
            x, y, width, height = args

            self.x = x
            self.y = y

            self.width = width
            self.height = height
        elif len(kwargs) == 4 and len(args) == 0:
            self.x = kwargs['x']
            self.y = kwargs['y']

            self.width = kwargs['width']
            self.height = kwargs['height']
        elif len(args) == 0 and len(kwargs) == 0:
            self.x = 0
            self.y = 0

            self.width = \
            self.height = pygame.display.get_window_size()
        else:
            raise Exception("No matching overload")

        Attacher.__init__(self)
        Parented.__init__(self)
        Hoverable.__init__(self)
        Initializable.__init__(self)
        MiniStyleable.__init__(self)

    ##################
    ## AUTO REFRESH ##
    ##################

    def onAttached(self) -> None:
        if (refresh := self.refreshTime()) is not None:
            parent = self.parent

            def refresher():
                nonlocal self, refresh, parent

                time.sleep(refresh)

                while True:
                    if self.parent != parent:
                        break

                    if self.pendingRerender():
                        pygame.event.post(pygame.event.Event(0))

                    time.sleep(self.refreshTime())

            Thread(target=refresher, daemon=True).start()

    #############
    ## GETTERS ##
    #############

    def get_rect(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)

    ############
    ## LAYOUT ##
    ############

    def lay(self) -> None:
        pass

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

    def refreshTime(self) -> int|None:
        return None

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

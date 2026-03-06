import pygame

from ..iwidget.IWidget import IWidget
from ..iwidget.IAttacher import IAttacher
from ..iwidget.IRenderable import IRenderable

from .Initializable import Initializable

from abc import ABCMeta
from typing import final, overload

class Container(Initializable, IWidget, metaclass=ABCMeta):
    x: int
    y: int

    width: int
    height: int

    _renderables: list[IRenderable]
    _attachers: list[IAttacher]

    @overload
    def __init__(self, x: int, y: int, width: int, height: int, /):
        ...

    @overload
    def __init__(self):
        ...

    def __init__(self, *params):
        super().__init__()

        if len(params) == 4:
            x, y, width, height = params

            self.x = x
            self.y = y

            self.width = width
            self.height = height
        elif len(params) == 0:
            self.x = 0
            self.y = 0

            self.width = pygame.display.get_surface().get_width()
            self.height = pygame.display.get_surface().get_height()
        else:
            raise Exception("No matching overload")

        self._renderables = []
        self._attachers = []

    ##########################
    ## SUB PENDING RENDERER ##
    ##########################

    def anyChanged(self) -> bool:
        for widget in self._renderables:
            if widget.anyChanged():
                return True

        return False

    ###############
    ## RENDERING ##
    ###############

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        for widget in self._renderables:
            widget.render(surface.subsurface(self.x, self.y, self.width, self.height))

    def renderChanged(self, surface: pygame.Surface) -> None:
        if self.pendingRerender():
            self.render(surface)
        else:
            for widget in self._renderables:
                widget.renderChanged(surface.subsurface(self.x, self.y, self.width, self.height))

            if self.anyChanged():
                pygame.display.flip()

    ###########
    ## MOUSE ##
    ###########

    def mouseMoved(self, x: int, y: int) -> None:
        for widget in self._attachers:
            widget.mouseMoved(x, y)

    def mousePressed(self, x: int, y: int, button: int) -> None:
        for widget in self._attachers:
            widget.mousePressed(x, y, button)

    def mouseReleased(self, x: int, y: int, button: int) -> None:
        for widget in self._attachers:
            widget.mouseReleased(x, y, button)

    ##############
    ## KEYBOARD ##
    ##############

    def keyPressed(self, key: int, unicode: str) -> None:
        for widget in self._attachers:
            widget.keyPressed(key, unicode)

    def keyReleased(self, key: int, unicode: str) -> None:
        for widget in self._attachers:
            widget.keyReleased(key, unicode)

    #############
    ## WIDGETS ##
    #############

    def addRenderable(self, renderable: IRenderable) -> None:
        self._renderables.append(renderable)

    def addAttacher(self, attacher: IAttacher) -> None:
        self._attachers.append(attacher)

    @final
    def addREWidget(self, widget: IWidget) -> None:
        self.addRenderable(widget)
        self.addAttacher(widget)

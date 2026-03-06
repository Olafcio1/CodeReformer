import pygame

from ..iwidget.IWidget import IWidget
from ..iwidget.IAttacher import IAttacher
from ..iwidget.IRenderable import IRenderable

from .Widget import Widget
from .Initializable import Initializable

from .universal.Parented import Parented
from .universal.Represented import Represented

from .composition.style.Styleable import Styleable

from abc import ABCMeta
from typing import final, overload

class Container(
        Initializable, Styleable,
        Parented, Represented,
        IWidget,
        metaclass=ABCMeta
):
    x: int
    y: int

    width: int
    height: int

    _renderables: list[IRenderable]
    _attachers: list[IAttacher]
    _widgets: list[IWidget]

    @overload
    def __init__(self, x: int, y: int, width: int, height: int, /):
        ...

    @overload
    def __init__(self):
        ...

    def __init__(self, *params):
        Initializable.__init__(self)
        Styleable.__init__(self)
        Parented.__init__(self)

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
        self._widgets = []

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
        super().applyPre(surface)

        for widget in self._renderables:
            widget.render(surface.subsurface(self.x, self.y, self.width, self.height))

        super().applyPost(surface)

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

        self._widgets.append(widget)

        widget.parent = self

    ##############
    ## CHILDREN ##
    ##############

    def clear(self) -> None:
        self._renderables = []
        self._attachers = []
        self._widgets = []

    def getText(self) -> str:
        return self.text

    ##########
    ## TEXT ##
    ##########

    @property
    def text(self) -> str:
        value = ""

        for el in self._widgets:
            value += el.getText()

        return value

    @text.setter
    def text(self, args: tuple[str, pygame.color.Color | tuple[int, int, int] | tuple[int, int, int, int] | int, pygame.font.Font]) -> None:
        value, color, font = args

        class text_widget(Widget):
            __parent = self

            def __init__(self):
                size = font.size(value)
                super().__init__(
                    (int) ((self.__parent.width - size[0])/2),
                    (int) ((self.__parent.height - size[1]) / 2),
                    *size
                )

            def renderWidget(self, surface: pygame.Surface) -> None:
                texture = font.render(value, True, color)
                surface.blit(texture, self.get_rect())

        self.clear()
        self.addREWidget(text_widget())

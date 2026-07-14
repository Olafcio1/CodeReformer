import pygame

from ..iwidget.IWidget import IWidget
from ..iwidget.IAttacher import IAttacher
from ..iwidget.IRenderable import IRenderable

from .Widget import Widget
from .Initializable import Initializable

from .universal.Parented import Parented
from .universal.Represented import Represented
from .universal.Clippable import Clippable
from .universal.Hoverable import Hoverable

from .composition.style.Styleable import Styleable

from abc import ABCMeta
from typing import TypedDict, NotRequired, Literal, Unpack, Self, final, overload

TextTuple = tuple[
                str,
                pygame.color.Color | tuple[int, int, int] | tuple[int, int, int, int] | int,
                pygame.font.Font
]

class Text(TypedDict):
    text: str
    color: int
    font: pygame.font.Font
    align: NotRequired[Literal["left"] | Literal["center"]]

TextArgs = TextTuple | tuple[Text]
TextArg  = TextTuple | Text

class Container(
        Initializable, Styleable,
        Clippable, Hoverable,
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
        Hoverable.__init__(self)
        Styleable.__init__(self)
        Parented.__init__(self)

        if len(params) == 4:
            x, y, width, height = params

            self.x = x
            self.y = y

            self.width = width
            self.height = height
        elif len(params) == 2:
            width, height = params

            self.x = 0
            self.y = 0

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

        self._forceRerender = False

    ##########################
    ## SUB PENDING RENDERER ##
    ##########################

    _forceRerender: bool

    def pendingRerender(self) -> bool:
        if self._forceRerender:
            self._forceRerender = False
            return True

        if super().pendingRerender():
            return True

        for widget in self._renderables:
            if widget.pendingRerender():
                return True

        return False

    def forceRender(self) -> None:
        self._forceRerender = True

    ###############
    ## RENDERING ##
    ###############

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        super().applyPre(surface)

        sub = self._clipsub(surface)
        for widget in self._renderables:
            widget.render(sub)

        super().applyPost(surface)

    def renderChanged(self, surface: pygame.Surface) -> None:
        if self.pendingRerender():
            self.render(surface)
        else:
            sub = self._clipsub(surface)
            for widget in self._renderables:
                widget.renderChanged(sub)

    ###########
    ## MOUSE ##
    ###########

    def mouseMoved(self, x: int, y: int) -> None:
        for widget in self._attachers:
            widget.mouseMoved(x - self.x, y - self.y)

    def mousePressed(self, x: int, y: int, button: int) -> None:
        if self.isHovered(x, y):
            for widget in self._attachers:
                widget.mousePressed(x - self.x, y - self.y, button)

    def mouseReleased(self, x: int, y: int, button: int) -> None:
        if self.isHovered(x, y):
            for widget in self._attachers:
                widget.mouseReleased(x - self.x, y - self.y, button)

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
        attacher.onAttached()

    @final
    def addREWidget(self, widget: IWidget) -> None:
        widget._Parented__self_parent = self  # type: ignore

        self.addRenderable(widget)
        self.addAttacher(widget)

        self._widgets.append(widget)

    ####################
    ## WIDGETS\INSERT ##
    ####################

    def insertRenderable(self, renderable: IRenderable, index: int) -> None:
        self._renderables.insert(index, renderable)

    def insertAttacher(self, attacher: IAttacher, index: int) -> None:
        self._attachers.insert(index, attacher)
        attacher.onAttached()

    @final
    def insert(self, widget: IWidget, index: int) -> None:
        widget._Parented__self_parent = self  # type: ignore

        before = self._widgets[index]

        self.insertRenderable(widget, self._renderables.index(before))
        self.insertAttacher(widget, self._attachers.index(before))

        self._widgets.insert(index, widget)

    @final
    def insertBefore(self, widget: IWidget, before: IWidget) -> None:
        widget._Parented__self_parent = self  # type: ignore

        self.insertRenderable(widget, self._renderables.index(before))
        self.insertAttacher(widget, self._attachers.index(before))

        self._widgets.insert(self._widgets.index(before), widget)

    ####################
    ## WIDGETS\REMOVE ##
    ####################

    @final
    def removeChild(self, widget: IWidget) -> None:
        self._renderables.remove(widget)
        self._attachers.remove(widget)

        self._widgets.remove(widget)

        widget._Parented__self_parent = None

        self.forceRender()

    ##############
    ## CHILDREN ##
    ##############

    def clear(self) -> None:
        self._renderables = []
        self._attachers = []
        self._widgets = []

    def getText(self) -> str:
        return self.text

    def setText(self, *value: Unpack[TextArgs]) -> Self:
        self.text = value
        return self

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
    def text(self, args: TextArg) -> None:
        if isinstance(args, tuple):
            value, color, font = args
            align = 'center'
        else:
            value = args['text']
            color = args['color']
            font  = args['font']
            align = args.get('align', "center")

        class text_widget(Widget):
            __parent = self

            def __init__(self):
                size = font.size(value)

                if align == 'center':
                    x = (self.__parent.width - size[0]) / 2
                else:
                    x = 0

                super().__init__(
                    (int) (x),
                    (int) ((self.__parent.height - size[1]) / 2),
                    *size
                )

            def renderWidget(self, surface: pygame.Surface) -> None:
                texture = font.render(value, True, color)
                surface.blit(texture, self.get_rect())

        self.clear()
        self.addREWidget(text_widget())

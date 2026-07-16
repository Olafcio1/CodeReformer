import pygame

from ....util.event.Event import Event
from ....util.event.EventManager import EventManager

from ..iwidget.IWidget import IWidget
from ..iwidget.IAttacher import IAttacher
from ..iwidget.IRenderable import IRenderable

from .Widget import Widget
from .Initializable import Initializable

from .text.Text import Text
from .text.TextValue import TextValue
from .text.TextWidget import TextWidget

from .universal.Parented import Parented
from .universal.Represented import Represented
from .universal.Clippable import Clippable
from .universal.Hoverable import Hoverable

from .composition.style.Styleable import Styleable

from abc import ABCMeta
from typing import TypedDict, NotRequired, Literal, Unpack, Final, Self, final, overload

TextTuple = tuple[
                str,
                pygame.color.Color | tuple[int, int, int] | tuple[int, int, int, int] | int,
                pygame.font.Font
]

TextArgs = TextTuple | tuple[Text]
TextArg  = TextTuple | Text

@final
class MouseDownEvent(Event):
    x: Final[int]
    y: Final[int]
    button: Final[int]

    def __init__(self, x: int, y: int, button: int):
        self.x = x
        self.y = y
        self.button = button

class Container(
        Initializable, Styleable,
        Clippable, Hoverable,
        Parented, Represented,
        EventManager,
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
    def __init__(self, width: int, height: int, /):
        ...

    @overload
    def __init__(self, *, x: int = 0, y: int = 0, width: int, height: int):
        ...

    @overload
    def __init__(self):
        ...

    def __init__(self, *params, **kwparams):
        Initializable.__init__(self)
        EventManager.__init__(self)
        Hoverable.__init__(self)
        Styleable.__init__(self)
        Parented.__init__(self)

        if len(params) == 0 and len(kwparams) == 0:
            # Container()

            self.x = 0
            self.y = 0

            self.width = pygame.display.get_surface().get_width()
            self.height = pygame.display.get_surface().get_height()

        elif len(kwparams) == 0:
            if len(params) == 4:
                # Container(x, y, width, height, /)

                x, y, width, height = params

                self.x = x
                self.y = y

                self.width = width
                self.height = height

            elif len(params) == 2:
                # Container(width, height, /)

                width, height = params

                self.x = 0
                self.y = 0

                self.width = width
                self.height = height

            else:
                raise Exception("No matching overload")
        else:
            self.x = kwparams.get('x', 0)
            self.y = kwparams.get('y', 0)

            try:
                self.width  = kwparams['width']
                self.height = kwparams['height']
            except KeyError:
                raise Exception("No matching overload")

            for key in params:
                if key not in ('x', 'y', 'width', 'height'):
                    raise Exception("No matching overload")

        self._renderables = []
        self._attachers = []
        self._widgets = []

        self._forceRerender = False

        self.map("mousedown", MouseDownEvent)

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

    def refreshTime(self) -> int|None:
        return None

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

    ############
    ## ATTACH ##
    ############

    def onAttached(self) -> None:
        pass

    ###########
    ## MOUSE ##
    ###########

    __lastHoverState: bool = False

    def mouseMoved(self, x: int, y: int) -> None:
        super().mouseMoved(x, y)

        hoverState = self.isHovered()
        if hoverState != self.__lastHoverState:
            self.__lastHoverState = hoverState
            self.forceRender()

        for widget in self._attachers:
            widget.mouseMoved(x - self.x, y - self.y)

    def mousePressed(self, x: int, y: int, button: int) -> None:
        if self.isHovered(x, y):
            self.fire(MouseDownEvent(x, y, button))

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

    ########################
    ## WIDGETS (INTERNAL) ##
    ########################

    def __prepareChild(self, widget: IWidget) -> None:
        if widget._Parented__self_parent is not None:
            widget.remove()

        widget._Parented__self_parent = self  # type: ignore

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
        self.__prepareChild(widget)

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
        self.__prepareChild(widget)

        before = self._widgets[index]

        self.insertRenderable(widget, self._renderables.index(before))
        self.insertAttacher(widget, self._attachers.index(before))

        self._widgets.insert(index, widget)

    @final
    def insertBefore(self, widget: IWidget, before: IWidget) -> None:
        self.__prepareChild(widget)

        self.insertRenderable(widget, self._renderables.index(before))
        self.insertAttacher(widget, self._attachers.index(before))

        self._widgets.insert(self._widgets.index(before), widget)

    #####################
    ## WIDGETS\REPLACE ##
    #####################

    @final
    def replaceChild(self, widget: IWidget, newWidget: IWidget) -> None:
        self._renderables[self._renderables.index(widget)] = newWidget
        self._attachers[self._attachers.index(widget)] = newWidget

        self._widgets[self._widgets.index(widget)] = newWidget

        widget._Parented__self_parent = None

        self.__prepareChild(newWidget)
        newWidget.onAttached()

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

    def index(self, child: IWidget) -> int:
        return self._widgets.index(child)

    def child(self, index: int) -> IWidget:
        return self._widgets[index]

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
    def text(self) -> TextValue:
        value = TextValue("", parent=self)

        for el in self._widgets:
            value += el.getText()

        return value

    @text.setter
    def text(self, args: TextArg) -> None:
        if args == Ellipsis:
            return

        if isinstance(args, tuple):
            value, color, font = args
            align = 'center'
        else:
            value = args['text']
            color = args['color']
            font  = args['font']
            align = args.get('align', "center")

        self.clear()
        self.addREWidget(TextWidget(value, color, font, align, \
                                    parent=self))

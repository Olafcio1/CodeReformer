from abc import ABCMeta
from ...iwidget.IContainer import IContainer

class Parented(metaclass=ABCMeta):
    __self_parent: IContainer|None

    def __init__(self):
        self.__self_parent = None

    @property
    def parent(self):
        return self.__self_parent

    def appendTo(self, container: IContainer) -> None:
        container.addREWidget(self)

    def before(self, widget: "Parented") -> None:
        self.parent.insertBefore(widget, self)

    def remove(self) -> None:
        parent = self.parent

        if parent is not None:
            parent.removeChild(self)

    def wrap(self, width: int|None = None, height: int|None = None, *, offsetX: int = 0, offsetY: int = 0) -> IContainer:
        \
          if width   is None: width  = self.width + offsetX
        elif offsetX != 0:    raise Exception("'offsetX' cannot be provided along with the 'width' parameter")

        \
          if height  is None: height = self.height + offsetY
        elif offsetY != 0:    raise Exception("'offsetY' cannot be provided along with the 'height' parameter")

        from ...widget.Container import Container

        container = Container(width, height)

        self.parent.replaceChild(self, container)

        container.addREWidget(self)

        return container

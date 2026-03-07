from abc import ABCMeta
from ...iwidget.IWidget import IWidget

class Represented(IWidget, metaclass=ABCMeta):
    def __str__(self) -> str:
        return type(self).__name__

    def __repr__(self) -> str:
        return ("%s(x={0.x!s}, y={0.y!s}; width={0.width!s}, height={0.height!s})" % (
            type(self).__name__
        )).format(self)

from typing import Generic, TypeVar, Self, Any
from ...iwidget.IWidget import IWidget

T = TypeVar('T', bound="IWidget", covariant=True)

class WidgetBuilder(Generic[T]):
    _cls: type[T]

    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]

    _pos: tuple[int, int]
    _size: tuple[int, int]

    def __init__(self, cls: type[T]):
        self._cls = cls

        self._args = ()
        self._kwargs = {}

        self._pos = (-1, -1)

    def args(self, *args) -> Self:
        self._args = args
        return self

    def kw(self, **kw) -> Self:
        self._kwargs = kw
        return self

    def pos(self, x: int, y: int) -> Self:
        self._pos = (x, y)
        return self

    def size(self, width: int, height: int) -> Self:
        self._size = (width, height)
        return self

    def build(self) -> T:
        widget = self._cls(
            self._pos[0], self._pos[1],
            self._size[0], self._size[1],
            *self._args,
            **self._kwargs
        )

        return widget

from typing import Callable, Protocol, TypeVar
from ..Event import Event

T = TypeVar('T', bound="Event", covariant=True)

class ListenerList(Protocol):
    def __contains__(self, index: type[T]) -> bool:
        ...

    def __getitem__(self, index: type[T]) -> list[Callable[[T], None]]:
        ...

    def __setitem__(self, index: type[T], value: list[Callable[[T], None]]) -> None:
        ...

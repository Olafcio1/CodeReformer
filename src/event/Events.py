from typing import TypeVar, Callable, Protocol, final

from .Event import Event
from .NoEventArgumentException import NoEventArgumentException

__all__ = ("EventManager",)

T = TypeVar('T', bound="Event", covariant=True)

class ListenerList(Protocol):
    def __contains__(self, index: type[T]) -> bool:
        ...

    def __getitem__(self, index: type[T]) -> list[Callable[[T], None]]:
        ...

    def __setitem__(self, index: type[T], value: list[Callable[[T], None]]) -> None:
        ...

@final
class EventManager:
    __listeners: ListenerList = {}  # type: ignore

    @classmethod
    def register(cls, method: Callable[[T], None]) -> None:
        event = cls.__getEvent(method)
        if event in cls.__listeners:
            cls.__listeners[event].append(method)
        else:
            cls.__listeners[event] = [method]

    @classmethod
    def fire(cls, event: T) -> None:
        if type(event) in cls.__listeners:
            listeners: list[Callable[[T], None]] \
                     = cls.__listeners[event]  # type: ignore

            for method in listeners:
                method(event)

    @classmethod
    def __getEvent(cls, method: Callable[[T], None]) -> type[T]:
        args = method.__annotations__
        for arg in args:
            if issubclass(value := args[arg], Event):
                return value  # pyright: ignore[reportReturnType]

        raise NoEventArgumentException("No argument found that extends Event")

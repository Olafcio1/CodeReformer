from typing import TypeVar, Callable, Protocol, Any, final, overload

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

EventTarget = Callable[[T], None] | object

@final
class EventManager:
    __listeners: ListenerList = {}  # type: ignore

    @classmethod
    @overload
    def register(cls, /, target: Callable[[T], None]) -> None:
        ...

    @classmethod
    @overload
    def register(cls, /, target: object) -> None:
        ...

    @classmethod
    def register(cls, target: EventTarget) -> None:
        if isinstance(method := target, Callable):
            event = cls.__getEvent(method)
            if event in cls.__listeners:
                cls.__listeners[event].append(method)
            else:
                cls.__listeners[event] = [method]
        elif isinstance(obj := target, object):
            search = type(obj) if isinstance(obj, type) else obj
            methods: dict[str, Any] \
                   = search.__dict__  # type: ignore

            for m in methods.values():
                if isinstance(m, Callable) and hasattr(m, '__eventhandler__'):
                    cls.register(m)
        else:
            raise Exception("No matching overload")

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

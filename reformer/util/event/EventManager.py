from typing import TypeVar, Callable, final

from .manager.ListenerList import ListenerList
from .manager.IEventManager import IEventManager

from .manager.composite.EMRegistration import EMRegistration
from .manager.composite.EMUnregistration import EMUnregistration

from .Event import Event
from .NoEventArgumentException import NoEventArgumentException

__all__ = ("EventManager",)

T = TypeVar('T', bound="Event", covariant=True)

@final
class EventManager(
        EMRegistration, EMUnregistration,
        IEventManager
):
    _listeners: ListenerList = {}  # type: ignore

    @classmethod
    def fire(cls, event: T) -> None:  # type: ignore
        if type(event) in cls._listeners:
            listeners: list[Callable[[T], None]] \
                     = cls._listeners[type(event)]  # type: ignore

            for method in listeners:
                method(event)

    @classmethod
    def _getEvent(cls, method: Callable[[T], None]) -> type[T]:
        args = method.__annotations__
        for arg in args:
            if issubclass(value := args[arg], Event):
                return value  # pyright: ignore[reportReturnType]

        raise NoEventArgumentException("No argument found that extends Event")

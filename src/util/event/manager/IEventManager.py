from .ListenerList import ListenerList
from ..Event import Event

from typing import Callable, Protocol, TypeVar, overload

T = TypeVar('T', bound="Event", covariant=True)

class IEventManager(Protocol):
    _listeners: ListenerList

    ##################
    ## REGISTRATION ##
    ##################

    @classmethod
    @overload
    def register(cls, /, target: Callable[[T], None]) -> None:
        ...

    @classmethod
    @overload
    def register(cls, /, target: object) -> None:
        ...

    ####################
    ## UNREGISTRATION ##
    ####################

    @classmethod
    @overload
    def unregister(cls, /, target: Callable[[T], None]) -> None:
        ...

    @classmethod
    @overload
    def unregister(cls, /, target: object) -> None:
        ...

    ##############
    ## INTERNAL ##
    ##############

    @classmethod
    def _getEvent(cls, method: Callable[[T], None]) -> type[T]:
        ...

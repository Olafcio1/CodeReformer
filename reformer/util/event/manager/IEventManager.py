from .ListenerList import ListenerList
from ..Event import Event

from typing import Callable, Protocol, TypeVar, overload

T = TypeVar('T', bound="Event", covariant=True)

class IEventManager(Protocol):
    _listeners: ListenerList

    ##################
    ## REGISTRATION ##
    ##################

    @overload
    def register(self, /, target: Callable[[T], None]) -> None:
        ...

    @overload
    def register(self, /, target: object) -> None:
        ...

    ####################
    ## UNREGISTRATION ##
    ####################

    @overload
    def unregister(self, /, target: Callable[[T], None]) -> None:
        ...

    @overload
    def unregister(self, /, target: object) -> None:
        ...

    ##############
    ## INTERNAL ##
    ##############

    def _getEvent(self, method: Callable[[T], None]) -> type[T]:
        ...

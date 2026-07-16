from typing import Callable, TypeVar, Any

from ..IEventManager import IEventManager
from ..EventTarget import EventTarget
from ...Event import Event

T = TypeVar('T', bound="Event", covariant=True)

class EMMapped(IEventManager):
    _mapping: dict[str, type]

    def __init__(self):
        self._mapping = {}

    def on(self, type: str, callback: Callable[[T], None]) -> None:
        if type not in self._mapping:
            raise Exception("%r not present" % type)

        self._listeners[self._mapping[type]].append(callback)

    def map(self, name: str, type: type) -> None:
        if name in self._mapping:
            raise Exception("%r already present" % name)

        self._mapping[name] = type
        self._listeners[type] = []

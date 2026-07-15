from typing import Callable, TypeVar, Any

from ..IEventManager import IEventManager
from ..EventTarget import EventTarget
from ...Event import Event

T = TypeVar('T', bound="Event", covariant=True)

class EMRegistration(IEventManager):
    def register(self, target: EventTarget) -> None:
        if isinstance(method := target, Callable):
            event = self._getEvent(method)

            if event in self._listeners:
                self._listeners[event].append(method)
            else:
                self._listeners[event] = [method]
        elif isinstance(obj := target, object):
            search = obj if isinstance(obj, type) else type(obj)
            methods: dict[str, Any] \
                   = search.__dict__  # type: ignore

            for m in methods.values():
                if isinstance(m, Callable) and hasattr(m, '__eventhandler__'):
                    if not isinstance(obj, type):
                        underneath = m

                        m = lambda *args: underneath(obj, *args)
                        m.__annotations__ = underneath.__annotations__

                    self.register(m)
        else:
            raise Exception("No matching overload")

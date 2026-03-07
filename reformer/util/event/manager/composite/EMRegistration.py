from typing import Callable, TypeVar, Any

from ..IEventManager import IEventManager
from ..EventTarget import EventTarget
from ...Event import Event

T = TypeVar('T', bound="Event", covariant=True)

class EMRegistration(IEventManager):
    @classmethod
    def register(cls, target: EventTarget) -> None:
        if isinstance(method := target, Callable):
            event = cls._getEvent(method)

            if event in cls._listeners:
                cls._listeners[event].append(method)
            else:
                cls._listeners[event] = [method]
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

                    cls.register(m)
        else:
            raise Exception("No matching overload")

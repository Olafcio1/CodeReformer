from typing import Callable, Any

from ..EventTarget import EventTarget
from ..IEventManager import IEventManager

class EMUnregistration(IEventManager):
    @classmethod
    def unregister(cls, target: EventTarget) -> None:
        if isinstance(method := target, Callable):
            event = cls._getEvent(method)
            if event in cls._listeners:
                cls._listeners[event].remove(method)
            else:
                print("[EventManager/WARN] Failed to unregister %s(%s)" % (target, event.__name__))
        elif isinstance(obj := target, object):
            search = type(obj) if isinstance(obj, type) else obj
            methods: dict[str, Any] \
                   = search.__dict__  # type: ignore

            for m in methods.values():
                if isinstance(m, Callable) and hasattr(m, '__eventhandler__'):
                    cls.unregister(m)
        else:
            raise Exception("No matching overload")

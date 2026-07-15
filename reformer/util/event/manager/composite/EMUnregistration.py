from typing import Callable, Any

from ..EventTarget import EventTarget
from ..IEventManager import IEventManager

class EMUnregistration(IEventManager):
    def unregister(self, target: EventTarget) -> None:
        if isinstance(method := target, Callable):
            event = self._getEvent(method)
            if event in self._listeners:
                self._listeners[event].remove(method)
            else:
                print("[EventManager/WARN] Failed to unregister %s(%s)" % (target, event.__name__))
        elif isinstance(obj := target, object):
            search = type(obj) if isinstance(obj, type) else obj
            methods: dict[str, Any] \
                   = search.__dict__  # type: ignore

            for m in methods.values():
                if isinstance(m, Callable) and hasattr(m, '__eventhandler__'):
                    self.unregister(m)
        else:
            raise Exception("No matching overload")

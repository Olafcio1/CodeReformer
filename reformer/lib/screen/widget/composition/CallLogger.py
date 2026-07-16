from abc import ABCMeta
from types import ModuleType as module
from typing import Callable, Any

class CallLogger(metaclass=ABCMeta):
    __mod: module
    __set_properties: set[str]

    def __init__(self, mod: module):
        self.__mod = mod
        self.__set_properties = set()

    def isSet(self, prop: str) -> bool:
        return prop in self.__set_properties

    def __getattribute__(self, name: str):
        val = super().__getattribute__(name)

        if name.startswith("_"):
            return val

        if isinstance(val, Callable):
            if val.__globals__['__spec__'].name.startswith(self.__mod.__package__):
                return lambda *args, **kwargs: self.__wrap(val, args, kwargs)

        return val

    def __wrap(self, method: Callable, args: list, kwargs: dict):
        self.__set_properties.add(method.__name__)

        return method(*args, **kwargs)

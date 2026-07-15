from abc import ABCMeta
from typing import Callable, Any

from .key import StBackground

class CallLogger(metaclass=ABCMeta):
    __set_properties: set[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__set_properties = set()

    def isSet(self, prop: str) -> bool:
        return prop in self.__set_properties

    def __getattribute__(self, name: str):
        val = super().__getattribute__(name)

        if name.startswith("_"):
            return val

        if isinstance(val, Callable):
            if val.__globals__['__spec__'].name.startswith(StBackground.__package__):
                return lambda *args, **kwargs: self.__wrap(val, args, kwargs)

        return val

    def __wrap(self, method: Callable, args: list, kwargs: dict):
        self.__set_properties.add(method.__name__)

        return method(*args, **kwargs)

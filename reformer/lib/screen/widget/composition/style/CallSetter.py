from abc import ABCMeta
from typing import Protocol, Generic, Any, overload

from ..Backable import T

class IBackable(Protocol[T]):
    back: T

class CallSetter(Generic[T], IBackable[T], metaclass=ABCMeta):
    @overload
    def __call__(self, code: str, /) -> T:
        ...

    @overload
    def __call__(self, **properties: Any) -> T:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        if len(args) == 1 and len(kwargs) == 0:
            code = args[0]
            lines = code.splitlines()

            for line in lines:
                line = line.lstrip()
                if line == "":
                    continue

                key, _, value = line.partition(": ")

                key = key.strip()
                value = value.strip()

                key = self.__keyTransformation(key)

                if key.startswith("_") or \
                   not hasattr(self, key):
                    raise Exception("Tried to assign unexistent key %r" % key)

                getattr(self, key)(eval(value, {}, {}))
        elif len(args) == 0 and len(kwargs) >= 1:
            for key in kwargs:
                value = kwargs[key]

                getattr(self, key)(value)
        else:
            raise Exception("No matching overload")

        return self.back

    def __keyTransformation(self, key: str) -> str:
        out = ""
        upper = False

        for ch in key:
            if upper:
                out += ch.upper()
                upper = False
            elif ch == "_":
                upper = True
            else:
                out += ch

        return out

from abc import ABCMeta
from typing import Protocol, Generic

from ..Backable import T

class IBackable(Protocol[T]):
    back: T

class CallSetter(Generic[T], IBackable[T], metaclass=ABCMeta):
    def __call__(self, code: str) -> T:
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

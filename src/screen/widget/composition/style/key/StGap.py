from abc import ABCMeta
from typing import Self, overload

class StGap(metaclass=ABCMeta):
    _gap: int = 0

    @overload
    def gap(self) -> int:
        ...

    @overload
    def gap(self, value: int, /) -> Self:
        ...

    def gap(self, *params):
        if len(params) == 0:
            return self._gap
        elif len(params) == 1:
            self._gap = params[0]
            return self
        else:
            raise Exception("No matching overload")

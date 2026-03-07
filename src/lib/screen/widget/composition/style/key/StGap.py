from abc import ABCMeta
from typing import Self, overload

class StGap(metaclass=ABCMeta):
    _gapHorizontal: int = 0
    _gapVertical: int = 0

    @overload
    def gap(self) -> tuple[int, int]:
        ...

    @overload
    def gap(self, both: int, /) -> Self:
        ...

    @overload
    def gap(self, horizontal: int, vertical: int, /) -> Self:
        ...

    def gap(self, *params):
        if len(params) == 0:
            return (self._gapHorizontal, self._gapVertical)
        elif len(params) == 1:
            self._gapHorizontal = self._gapVertical = params[0]
            return self
        elif len(params) == 2:
            self._gapHorizontal, self._gapVertical = params
            return self
        else:
            raise Exception("No matching overload")

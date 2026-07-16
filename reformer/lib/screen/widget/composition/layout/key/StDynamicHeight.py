from abc import ABCMeta
from typing import Self, overload

class StDynamicHeight(metaclass=ABCMeta):
    _dynamicHeight: bool = False

    @overload
    def dynamicHeight(self) -> bool:
        ...

    @overload
    def dynamicHeight(self, value: bool, /) -> Self:
        ...

    def dynamicHeight(self, *params):
        if len(params) == 0:
            return self._dynamicHeight
        elif len(params) == 1:
            self._dynamicHeight = params[0]

            return self
        else:
            raise Exception("No matching overload")

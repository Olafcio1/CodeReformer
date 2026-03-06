from abc import ABCMeta
from typing import Literal, Self, overload

Display = Literal["non-managed", "grid", "flex"]

class StDisplay(metaclass=ABCMeta):
    _display: Display = "non-managed"

    @overload
    def display(self) -> Display:
        ...

    @overload
    def display(self, value: Display, /) -> Self:
        ...

    def display(self, *params):
        if len(params) == 0:
            return self._display
        elif len(params) == 1:
            self._display = params[0]
            return self
        else:
            raise Exception("No matching overload")

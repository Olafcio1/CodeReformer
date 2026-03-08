from abc import ABCMeta
from typing import Self, overload

class StMargin(metaclass=ABCMeta):
    _marginTop: int = 0
    _marginBottom: int = 0

    _marginLeft: int = 0
    _marginRight: int = 0

    @overload
    def margin(self) -> tuple[int, int, int, int]:
        ...

    @overload
    def margin(self, value: tuple[int, int, int, int], /) -> Self:
        ...

    def margin(self, *params):
        if len(params) == 0:
            return (
                self._marginTop,
                self._marginBottom,
                self._marginLeft,
                self._marginRight
            )
        elif len(params) == 1:
            self._marginTop, \
            self._marginBottom, \
            self._marginLeft, \
            self._marginRight = params[0]

            return self
        else:
            raise Exception("No matching overload")

    def marginTop(self, value: int) -> Self:
        self._marginTop = value
        return self

    def marginBottom(self, value: int) -> Self:
        self._marginBottom = value
        return self

    def marginLeft(self, value: int) -> Self:
        self._marginLeft = value
        return self

    def marginRight(self, value: int) -> Self:
        self._marginRight = value
        return self

from abc import ABCMeta
from typing import Self, overload

class StPadding(metaclass=ABCMeta):
    _paddingTop: int = 0
    _paddingBottom: int = 0

    _paddingLeft: int = 0
    _paddingRight: int = 0

    @overload
    def padding(self) -> tuple[int, int, int, int]:
        ...

    @overload
    def padding(self, value: tuple[int, int, int, int], /) -> Self:
        ...

    def padding(self, *params):
        if len(params) == 0:
            return (
                self._paddingTop,
                self._paddingBottom,
                self._paddingLeft,
                self._paddingRight
            )
        elif len(params) == 1:
            self._paddingTop, \
            self._paddingBottom, \
            self._paddingLeft, \
            self._paddingRight = params[0]

            return self
        else:
            raise Exception("No matching overload")

    def paddingTop(self, value: int) -> Self:
        self._paddingTop = value
        return self

    def paddingBottom(self, value: int) -> Self:
        self._paddingBottom = value
        return self

    def paddingLeft(self, value: int) -> Self:
        self._paddingLeft = value
        return self

    def paddingRight(self, value: int) -> Self:
        self._paddingRight = value
        return self

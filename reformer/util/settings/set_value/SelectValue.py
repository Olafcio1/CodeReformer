from typing import TypeVar, Generic, Final, final

T = TypeVar('T')

@final
class SelectValue(Generic[T]):
    """
    A select value.

    Should be shown as a clickable option, which after click,
    shows a menu popup - that displays other options, that
    when clicked, is set as the value.
    """

    options: Final[list[T]]
    value: T

    def __init__(self, defaultIndex: int, options: list[T]):
        self.options = options
        self.value = options[defaultIndex]

    def copy(self) -> "SelectValue[T]":
        return SelectValue[T](self.options.index(self.value), self.options)

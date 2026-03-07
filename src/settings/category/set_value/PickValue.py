from typing import TypeVar, Generic, Final, final

T = TypeVar('T')

@final
class PickValue(Generic[T]):
    """
    A pick value.

    This is equivalent to `SelectValue` on setting-level.

    It differs only in UI: a pick value should show its options
    in a flex element, and if some doesn't fit, they should be
    shown as a select menu popup when clicked on an ellipsis
    (`...`) option.
    """

    options: Final[list[T]]
    value: T

    def __init__(self, defaultIndex: int, options: list[T]):
        self.options = options
        self.value = options[defaultIndex]

from typing import final

@final
class BoolValue:
    """
    A bool value.

    Should be shown as a clickable option, which after click,
    toggles its active state.
    """

    value: bool

    def __init__(self, defaultValue: bool):
        self.value = defaultValue

    def copy(self) -> "BoolValue":
        return BoolValue(self.value)

from typing import Generic, TypeVar, Final, final

from .set_value.StringValue import StringValue
from .set_value.SelectValue import SelectValue
from .set_value.PickValue import PickValue

SettingValue = StringValue | SelectValue | PickValue
T = TypeVar('T', bound="SettingValue")

@final
class Setting(Generic[T]):
    name: Final[str]
    value: Final[T]

    def __init__(self, /, name: str, value: T) -> None:
        self.name = name
        self.value = value

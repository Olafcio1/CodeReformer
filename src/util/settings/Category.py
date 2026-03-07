from typing import final
from .Setting import Setting, SettingValue

@final
class Category:
    name: str
    settings: dict[str, Setting]

    def __init__(self, /, name: str, **settings: SettingValue) -> None:
        self.name = name
        self.settings = {}

        for name in settings:
            self.settings[name] = Setting(name, settings[name])

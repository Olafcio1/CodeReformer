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
            self.settings[name] = Setting(self.__humanize(name), settings[name])

    @staticmethod
    def __humanize(name: str) -> str:
        out = ""
        lastUpper = True
        first = True

        for ch in name:
            if first:
                out += ch.upper()
                first = False

                continue
            elif ch.isupper() and not lastUpper:
                out += " "
                out += ch.upper()
            else:
                out += ch

            lastUpper = ch.isupper()

        return out

    def copy(self) -> "Category":
        category = Category(self.name)
        for key, value in self.settings.items():
            category.settings[key] = value.copy()

        return category

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
        word = True
        lastUpper = True

        for ch in name:
            if ch.isupper() != lastUpper:
                if not word:
                    out += " "

                out += ch.upper()
                lastUpper = ch.isupper()
            else:
                out += ch
                word = False

        return out

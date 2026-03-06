from typing import final
from ..screen.Screen import Screen

@final
class StaticRendering:
    def __init__(self):
        raise Exception("Initialization not permitted")

    @staticmethod
    def getScreen() -> Screen:
        ...

    @staticmethod
    def setScreen(value: Screen) -> None:
        ...

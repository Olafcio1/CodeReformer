from typing import Final

from .Generator import Generator
from ....util.event import Event

class GeneratorsEvent(Event):
    __generators: Final[list[Generator]]

    def __init__(self) -> None:
        self.__generators = []

    def add(self, generator: Generator) -> None:
        self.__generators.append(generator)

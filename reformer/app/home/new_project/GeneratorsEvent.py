import pygame
from typing import Protocol, Final

from .Generator import Generator
from ....util.event import Event

class GeneratorType(Protocol):
    def __call__(self) -> Generator:
        ...

    @staticmethod
    def getName() -> str:
        ...

    @staticmethod
    def getIcon() -> pygame.Surface:
        ...

class GeneratorsEvent(Event):
    __generators: Final[list[GeneratorType]]

    def __init__(self) -> None:
        self.__generators = []

    def add(self, generator: GeneratorType) -> None:
        self.__generators.append(generator)

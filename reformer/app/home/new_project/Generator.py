import pygame

from abc import ABCMeta, abstractmethod
from typing import Final, _GenericAlias  # type: ignore

from ....util.settings.Category import Category

class Generator(metaclass=ABCMeta):
    __name: str
    __icon: pygame.Surface
    __categories: Final[dict[str, Category]]

    def __init__(self, name: str, icon: pygame.Surface) -> None:
        self.__name = name
        self.__icon = icon
        self.__categories = {}

        for key in self.__annotations__:
            Type = self.__annotations__[key]
            if type(Type) == _GenericAlias:
                Type = Type.__args__[0]

            if issubclass(Type, Category):
                self.__categories[key] = self.__dict__[key]

    #############
    ## GETTERS ##
    #############

    def getName(self) -> str:
        return self.__name

    def getIcon(self) -> pygame.Surface:
        return self.__icon

    def getCategories(self) -> dict[str, Category]:
        return self.__categories

    ##############
    ## ABSTRACT ##
    ##############

    @abstractmethod
    def create(self, path: str) -> None:
        ...

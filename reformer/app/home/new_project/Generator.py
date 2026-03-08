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

        cls = type(self)
        members = {**cls.__dict__}  # Fixes 'RuntimeError: dictionary changed during iteration'

        for key in members:
            Value = members[key]
            Type = cls.__annotations__.get(key, type(Value))

            if type(Type) == _GenericAlias:
                Type = Type.__args__[0]

            if issubclass(Type, Category):
                self.__categories[key] = Value

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

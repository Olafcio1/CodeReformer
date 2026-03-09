import pygame

from abc import ABCMeta, abstractmethod
from typing import Final, ClassVar, Callable, TypedDict, _GenericAlias  # type: ignore

from ....util.settings.Category import Category

class GeneratorMetadata(TypedDict):
    name: Callable[[], str]
    icon: Callable[[], pygame.Surface]

class Generator(metaclass=ABCMeta):
    __metadata__: ClassVar[GeneratorMetadata]
    __categories: Final[dict[str, Category]]

    def __init__(self) -> None:
        self.__categories = {}

        cls = type(self)
        members = {**cls.__dict__}  # Fixes 'RuntimeError: dictionary changed during iteration'

        for key in members:
            Value = members[key]
            Type = cls.__annotations__.get(key, type(Value))

            if type(Type) == _GenericAlias:
                Type = Type.__args__[0]

            if issubclass(Type, Category):
                Value: Category
                self.__categories[key] = Value.copy()

    #############
    ## GETTERS ##
    #############

    @classmethod
    def getName(cls) -> str:
        return cls.__metadata__['name']()

    @classmethod
    def getIcon(cls) -> pygame.Surface:
        return cls.__metadata__['icon']()

    def getCategories(self) -> dict[str, Category]:
        return self.__categories

    ##############
    ## ABSTRACT ##
    ##############

    @abstractmethod
    def create(self, path: str) -> None:
        ...

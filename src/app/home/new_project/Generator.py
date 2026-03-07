from abc import ABCMeta, abstractmethod
from typing import Final

from ....util.settings.Category import Category

class Generator(metaclass=ABCMeta):
    __name: str
    __categories: Final[dict[str, Category]]

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__categories = {}

        for key in self.__dict__:
            if issubclass(self.__annotations__[key], Category):
                self.__categories[key] = self.__dict__[key]

    #############
    ## GETTERS ##
    #############

    def getName(self) -> str:
        return self.__name

    def getCategories(self) -> dict[str, Category]:
        return self.__categories

    ##############
    ## ABSTRACT ##
    ##############

    @abstractmethod
    def create(self, path: str) -> None:
        ...

import pygame

from ..iwidget.IRenderable import IRenderable
from abc import ABCMeta, abstractmethod

class Initializable(IRenderable, metaclass=ABCMeta):
    ## INITIALIZATION ##

    __initialized: bool

    def __init__(self):
        self.__initialized = False

    def init(self) -> None:
        pass

    ## PENDING RENDERER ##

    def pendingRerender(self) -> bool:
        return not self.__initialized

    def anyChanged(self) -> bool:
        return self.pendingRerender()

    ## WRAPPERS ##

    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        if not self.__initialized:
            self.__initialized = True
            self.init()

    def renderChanged(self, surface: pygame.Surface) -> None:
        if self.pendingRerender():
            self.render(surface)

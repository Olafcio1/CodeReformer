import pygame

from .Widget import Widget

from abc import ABCMeta, abstractmethod
from typing import final

class ClippedWidget(Widget, metaclass=ABCMeta):
    @final
    def renderWidget(self, surface: pygame.Surface) -> None:
        self.renderClipped(surface.subsurface(
            self.x, self.y,
            self.width, self.height
        ))

        #pygame.display.update(self.get_rect())  ---   update(...) doesn't work on subsurfaces

    @abstractmethod
    def renderClipped(self, surface: pygame.Surface) -> None:
        ...

    def get_clipped_rect(self) -> tuple[int, int, int, int]:
        return (0, 0, self.width, self.height)

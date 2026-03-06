import pygame

from .Widget import Widget
from ..UIError import UIError

from abc import ABCMeta, abstractmethod
from typing import final

class ClippedWidget(Widget, metaclass=ABCMeta):
    @final
    def renderWidget(self, surface: pygame.Surface) -> None:
        try:
            sub = surface.subsurface(
                self.x, self.y,
                self.width, self.height
            )
        except ValueError:
            xOverflow = self.width > surface.get_width()
            yOverflow = self.height > surface.get_height()

            err = UIError("Tried to draw outside of the boundaries; consider expanding the parent %s's %s" % (
                self.parent,

                'size' if (xOverflow and yOverflow) else \
                'width' if xOverflow else \
                'height'
            ))


            raise err

        self.renderClipped(sub)

        #pygame.display.update(self.get_rect())  ---   update(...) doesn't work on subsurfaces

    @abstractmethod
    def renderClipped(self, surface: pygame.Surface) -> None:
        ...

    def get_clipped_rect(self) -> tuple[int, int, int, int]:
        return (0, 0, self.width, self.height)

import pygame

from ...iwidget.IWidget import IWidget
from ...UIError import UIError

from abc import ABCMeta

class Clippable(IWidget, metaclass=ABCMeta):
    def _clipsub(self, surface: pygame.Surface) -> pygame.Surface:
        try:
            return surface.subsurface(
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

            err.__cause__ = None
            err.__context__ = None

            err.__suppress_context__ = True

            raise err

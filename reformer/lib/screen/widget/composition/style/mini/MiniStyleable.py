import pygame

from .MiniStyle import MiniStyle
from .....iwidget.IWidget import IWidget

from typing import Self

class MiniStyleable(IWidget):
    style: MiniStyle[Self]

    def __init__(self):
        self.style = MiniStyle(self)

    def applyPre(self, surface: pygame.Surface) -> None:
        if self.style._background != None:
            surface.fill(self.style._background, (self.x, self.y, self.width, self.height))

    def applyPost(self, surface: pygame.Surface) -> None:
        if self.style._borderTop    != None: surface.fill(self.style._borderTop, (self.x, self.y, self.width, 1))
        if self.style._borderBottom != None: surface.fill(self.style._borderBottom, (self.x, self.y + self.height - 1, self.width, 1))

        if self.style._borderLeft  != None: surface.fill(self.style._borderLeft, (self.x, self.y, 1, self.height))
        if self.style._borderRight != None: surface.fill(self.style._borderRight, (self.x + self.width - 1, self.y, 1, self.height))

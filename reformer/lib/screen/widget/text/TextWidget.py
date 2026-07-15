import pygame

from typing import Literal

from ..Widget import Widget
from ...iwidget.IContainer import IContainer

class TextWidget(Widget):
    value: str
    color: int

    font: pygame.font.Font

    def __init__(
            self,
            value: str, color: int,
            font: pygame.font.Font,
            align: Literal["left"] | Literal["center"],
            *,
            parent: IContainer
    ):
        self.font  = font
        self.value = value
        self.color = color

        size = font.size(value)

        if align == 'center':
            x = (parent.width - size[0]) / 2
        else:
            x = 0

        super().__init__(
            (int) (x),
            (int) ((parent.height - size[1]) / 2),
            *size
        )

    def renderWidget(self, surface: pygame.Surface) -> None:
        texture = self.font.render(self.value, True, self.color)
        surface.blit(texture, self.get_rect())

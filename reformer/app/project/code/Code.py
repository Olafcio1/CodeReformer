import pygame
import os

from ....lib.screen.widget.ClippedWidget import ClippedWidget
from ....resources import ResourceManager

from typing import Callable

class Code(ClippedWidget):
    lines: list[str]

    font:     pygame.font.Font
    font_num: pygame.font.Font

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.style.background(0x333433)
        self.style.border((0x555655, 0x555655, 0x555655, 0x555655))

        self.lines = []

        self.font     = ResourceManager.font['/font/0xProtoNerdFontMono-Regular.ttf:-2']
        self.font_num = ResourceManager.font['/font/0xProtoNerdFontMono-Regular.ttf:-2']

        self.scrollY = 0

    scrollY: int

    def renderClipped(self, surface: pygame.Surface) -> None:
        if not self.lines:
            return

        i = 1
        y = self.scrollY

        gap    = 2
        padTop = 3

        y += padTop

        numwidth = 10 + self.font_num.size("8" * len(str(len(self.lines))))[0]
        surface.fill(0x282928, (0, 0, numwidth, self.height))

        for line in self.lines:
            surface.blit(self.font_num.render(str(i), True, 0xafafafff), (6, y+2))
            surface.blit(self.font    .render(line,   True, 0xffffffff), (numwidth + 3, y+2))

            i += 1
            y += 18 + gap

            if y >= self.height:
                return

    def mouseScroll(self, x: float, y: float) -> None:
        if self.isHovered():
            self.scrollY = max(len(self.lines) * -16 - 1, min(0, self.scrollY + int(y*((18+2)*3))))
            self.forceRender()

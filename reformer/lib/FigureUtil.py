import pygame
from typing import final

@final
class FigureUtil:
    def __init__(self):
        raise Exception("Initialization not permitted")

    @staticmethod
    def roundedRect_fill(surface: pygame.Surface, color: int, pos: tuple[int, int, int, int]) -> None:
        width = pos[2]
        height = pos[3]

        startX = pos[0]
        startY = pos[1]

        endY = startY + height - 3
        startY += 3

        for r in range(3):
            x = startX + r

            surface.fill(color, (x, startY - r, width - r, 1))
            surface.fill(color, (startX, endY + r, width - r, 1))

        for y in range(startY, endY):
            surface.fill(color, (startX, y, width, 1))

    @staticmethod
    def roundedRect_stroke(surface: pygame.Surface, color: int, pos: tuple[int, int, int, int]) -> None:
        x, y, \
        w, h = pos

        surface.fill(color, (x + 3, y, w - 3, 1))

        for i in range(h):
            yVal = y + i

            # Left-Top
            lt = max(0, 3 - i)
            surface.set_at((x + lt, yVal), color)

            # Right-Bottom
            rb = max(0, i - (h - 3))
            surface.set_at((x + w - 1 - rb, yVal), color)

        surface.fill(color, (x, y + h, w - 3, 1))

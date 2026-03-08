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

        for r in range(3):
            x = startX + r
            rY = 3 - r

            surface.fill(color, (x, startY + rY, width - r, 1))
            surface.fill(color, (startX, endY - rY, width - r, 1))

        for y in range(startY + 3, endY - 3):
            surface.fill(color, (startX, y, width, 1))

    @staticmethod
    def roundedRect_stroke(surface: pygame.Surface, color: int, pos: tuple[int, int, int, int]) -> None:
        pygame.draw.rect(surface, color, pos, 1)

        x, y, \
        w, h = pos

        for i in range(3):
            # Left-Top
            surface.set_at((x + i, y), 0x333433)
            surface.set_at((x, y + i), 0x333433)

            surface.set_at((x + (3 - i), y + i), color)

            # Right-Bottom
            surface.set_at((x + w - 1 - i, y + h - 1), 0x333433)
            surface.set_at((x + w - 1, y + h - 1 - i), 0x333433)

            surface.set_at((x + w - 1 - i, y + h - (3 - i + 1)), color)

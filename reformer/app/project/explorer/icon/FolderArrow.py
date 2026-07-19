import pygame
from .....lib.screen.widget.ClippedWidget import ClippedWidget

class FolderArrow(ClippedWidget):
    right: int
    listener: ...

    def __init__(self, *args, right: int, listener: ..., **kwargs):
        super().__init__(*args, **kwargs)

        self.right = right
        self.listener = listener

    @staticmethod
    def quintic(num: float) -> float:
        return 1 - ((1 - num) ** 5)

    def renderClipped(self, surface: pygame.Surface) -> None:
        size = min(self.height, self.width)

        x = self.width  - size - self.right
        y = self.height - size

        if self.listener.is_open():
            y -= 2

            pygame.draw.lines(surface, 0x777877, closed=False, points=[
                (x + size/4,    y + size/2),
                (x + size/2,    y + size/1.25),
                (x + size/1.25, y + size/2)
            ])
        else:
            pygame.draw.lines(surface, 0x777877, closed=False, points=[
                (x + size/2,    y + size/4),
                (x + size/1.25, y + size/2),
                (x + size/2,    y + size/1.25)
            ])

import pygame
from .....lib.screen.widget.ClippedWidget import ClippedWidget

class FileIcon(ClippedWidget):
    @staticmethod
    def quintic(num: float) -> float:
        return 1 - ((1 - num) ** 5)

    def renderClipped(self, surface: pygame.Surface) -> None:
        pygame.draw.lines(surface, 0x777877, closed=True, points=[
            (self.width/6, self.height - 1),
            (self.width/6, 0),
            (self.width/1.16, 0),
            (self.width/1.16, self.height - 5),
            (self.width/2, self.height - 1)
        ])

        pygame.draw.line(surface, 0x777877, (self.width/6 + 3, 3), (self.width/1.16 - 3, 3))
        pygame.draw.line(surface, 0x777877, (self.width/6 + 3, 6), (self.width/1.16 - 3, 6))

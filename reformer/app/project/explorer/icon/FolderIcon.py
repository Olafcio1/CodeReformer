import pygame
from .....lib.screen.widget.ClippedWidget import ClippedWidget

class FolderIcon(ClippedWidget):
    @staticmethod
    def quintic(num: float) -> float:
        return 1 - ((1 - num) ** 5)

    def renderClipped(self, surface: pygame.Surface) -> None:
        pygame.draw.aalines(surface, 0x777877, closed=True, points=[
            (0, self.height/2                    + 3),
            (0, 4                                + 3),
            (4, 4                                + 3),
            (7, 0                                + 3),
            (self.width - 1, 0                   + 3),
            (self.width - 1, self.height/1.2 - 1 + 3),
            (0, self.height/1.2 - 1              + 3)
        ])

import pygame
from .widget.Container import Container

class Screen(Container):
    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        pygame.display.flip()

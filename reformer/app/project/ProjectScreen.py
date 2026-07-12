import pygame

from ...lib.screen.Screen import Screen
from ...lib.screen.widget.Initializable import Initializable

from typing import Callable

class ProjectScreen(Screen):
    class Background(Initializable):
        def render(self, surface: pygame.Surface) -> None:
            super().render(surface)
            surface.fill(0x333433)
            #pygame.display.flip()

    baseDir: str

    def __init__(self, baseDir: str):
        super().__init__()

        self.baseDir = baseDir

    def init(self) -> None:
        self.addRenderable(ProjectScreen.Background())

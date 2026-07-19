import pygame

from .explorer.Explorer import Explorer

from ...lib.screen.Screen import Screen
from ...lib.screen.widget.Widget import Widget

class ProjectScreen(Screen):
    class Background(Widget):
        def renderWidget(self, surface: pygame.Surface) -> None:
            surface.fill(0x333433)

    baseDir: str

    def __init__(self, baseDir: str):
        super().__init__()

        self.baseDir = baseDir

    def init(self) -> None:
        self.addRenderable(ProjectScreen.Background())
        self.addREWidget(Explorer(self.baseDir, x=10, y=10, \
                                                width=160, height=self.height - 20))

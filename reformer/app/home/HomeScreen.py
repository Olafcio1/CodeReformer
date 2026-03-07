import pygame

from .new_project.NewProjectScreen import NewProjectScreen
from .vsc_clone.CloneScreen import CloneScreen
from ..settings.SettingsScreen import SettingsScreen

from ...resources import ResourceManager

from ...lib.screen.Screen import Screen
from ...lib.screen.widget.Initializable import Initializable
from ...lib.screen.widget.ClippedWidget import ClippedWidget
from ...lib.screen.widget.Container import Container

from ...lib.static.StaticRendering import StaticRendering

from typing import Callable

class HomeScreen(Screen):
    class Background(Initializable):
        def render(self, surface: pygame.Surface) -> None:
            super().render(surface)
            surface.fill(0x333433)
            #pygame.display.flip()

    class Logo(ClippedWidget):
        def renderClipped(self, surface: pygame.Surface) -> None:
            texture = pygame.transform.smoothscale(
                ResourceManager.image['/image/logo.png'],
                self.get_size()
            )

            surface.blit(texture, (0, 0))
            pygame.draw.rect(surface, 0x202120, self.get_clipped_rect(), 1)

    class Button(ClippedWidget):
        text: str
        onClick: Callable[[], None]

        def __init__(
                self,
                /,
                x: int, y: int,
                width: int, height: int,
                *,
                text: str,
                onClick: Callable[[], None]
        ):
            super().__init__(x, y, width, height)

            self.text = text
            self.onClick = onClick

        def renderClipped(self, surface: pygame.Surface) -> None:
            # opera-gx style colors: #2c2a2a, #2f2d2d
            # think of making an opera like theme for this.
            # however, would a red IDE look good?
            # an orange one does (imo) - i use `Bearded Theme Coffee` for `VS Code`

            surface.fill(0x2a2a2a, (0, 0, self.width, (int) (self.height / 2)))
            surface.fill(0x2d2d2d, (0, (int) (self.height / 2), self.width, (int) (self.height / 2)))

            pygame.draw.rect(surface, 0x202120, self.get_clipped_rect(), 1)

            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.text)

            surface.blit(font.render(self.text, True, 0x59595fff), ((self.width - size[0])/2, (self.height - size[1])/2))

        def getText(self) -> str:
            return self.text

        def mousePressed(self, x: int, y: int, button: int) -> None:
            if self.isHovered(x, y):
                self.onClick()

    def init(self) -> None:
        self.addRenderable(HomeScreen.Background())
        self.addREWidget(HomeScreen.Logo(
            (int) (self.width/14),
            (int) (self.height/7),
            (int) (1024/4.4), (int) (403/4.4)
        ))

        self.addREWidget(btns := Container(
            (int) (self.width/14),
            (int) (self.height/7 + 403/4.4 - 1),
            (int) (1024/4.4),
            (int) (200)
        ).style
            .display("grid")
            .gap(8)
            .paddingTop(8)
         .back)

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="New Project", onClick=HomeScreen.Actions.newProject)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Open Project", onClick=HomeScreen.Actions.openProject)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Clone from VSC", onClick=HomeScreen.Actions.cloneFromVSC)
                                        .size((int) (1024/4.4), 24)
                                   .build())

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="Settings", onClick=HomeScreen.Actions.openSettings)
                                        .size((int) (1024/4.4), 24)
                                   .build())

    class Actions:
        @classmethod
        def newProject(cls) -> None:
            StaticRendering.setScreen(NewProjectScreen())

        @classmethod
        def openProject(cls) -> None:
            raise NotImplemented

        @classmethod
        def cloneFromVSC(cls) -> None:
            StaticRendering.setScreen(CloneScreen())

        @classmethod
        def openSettings(cls) -> None:
            StaticRendering.setScreen(SettingsScreen())

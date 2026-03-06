import pygame

from ..resources import ResourceManager

from ..screen.Screen import Screen
from ..screen.widget.Initializable import Initializable
from ..screen.widget.ClippedWidget import ClippedWidget
from ..screen.widget.Container import Container

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
            # 2a, 2f

            surface.fill(0x2a2a2a, (0, 0, self.width, (int) (self.height / 2)))
            surface.fill(0x2d2d2d, (0, (int) (self.height / 2), self.width, (int) (self.height / 2)))

            pygame.draw.rect(surface, 0x202120, self.get_clipped_rect(), 1)

            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.text)

            surface.blit(font.render(self.text, True, 0x59595fff), ((self.width - size[0])/2, (self.height - size[1])/2))

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
            (int) (100)
        ))

        btns.addREWidget(HomeScreen.Button.Builder()
                                        .kw(text="New Project", onClick=self.newProject)
                                        .pos(0, 12)
                                        .size((int) (1024/4.4), 24)
                                   .build())

    def newProject(self) -> None:
        ...

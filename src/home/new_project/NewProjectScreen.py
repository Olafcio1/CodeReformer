import pygame

from ...resources import ResourceManager

from ...screen.Screen import Screen

from ...screen.widget.Container import Container
from ...screen.widget.ClippedWidget import ClippedWidget

class NewProjectScreen(Screen):
    def init(self) -> None:
        window = Container()
        window.style.display("grid")
        window.style.background(0x333433)

        titlebar = Container(0, 0, self.width, 30)
        # titlebar.style.borderBottom()
        titlebar.text = ("New Project", 0xcfcfcfff, ResourceManager.font["/font/LEXEND.TTF"])

        content = Container(0, 30, self.width, self.height - 30)
        content.style.display("flex")

        content.addREWidget(self.makeGeneratorsContainer())
        content.addREWidget(self.makeFormContainer())

        window.addREWidget(titlebar)
        window.addREWidget(content)

        self.addREWidget(window)

    class GeneratorButton(ClippedWidget):
        name: str

        def __init__(
                self,
                x: int, y: int,
                width: int, height: int,
                *,
                name: str
        ):
            super().__init__(x, y, width, height)
            self.name = name

        def renderClipped(self, surface: pygame.Surface) -> None:
            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.name)

            surface.blit(font.render(self.name, True, 0x4f4f4f), (30, (self.height - size[1])/2))

    def makeGeneratorsContainer(self) -> Container:
        el = Container(0, 0, 150, self.height - 30)
        el.style.display("grid")

        el.addREWidget(NewProjectScreen.GeneratorButton.Builder()
                                                            .kw(name="Paper")
                                                            .size(100, 24)
                                                        .build())

        return el

    def makeFormContainer(self) -> Container:
        el = Container(0, 0, self.width - 150, self.height - 30)
        return el

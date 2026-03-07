import pygame

from ....resources import ResourceManager
from ....util.event import EventManager

from ....lib.screen.Screen import Screen

from ....lib.screen.widget.Container import Container
from ....lib.screen.widget.ClippedWidget import ClippedWidget

from .Generator import Generator
from .GeneratorsEvent import GeneratorsEvent

class NewProjectScreen(Screen):
    def init(self) -> None:
        window = Container()
        window.style.display("grid")
        window.style.background(0x333433)

        titlebar = Container(0, 0, self.width, 30)
        titlebar.style.borderBottom(0x222322)
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
        icon: pygame.Surface

        def __init__(
                self,
                x: int, y: int,
                width: int, height: int,
                *,
                name: str,
                icon: pygame.Surface
        ):
            super().__init__(x, y, width, height)

            self.name = name
            self.icon = pygame.transform.smoothscale(icon, (min(25, self.height - 5), min(25, self.height - 5)))

        def renderClipped(self, surface: pygame.Surface) -> None:
            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.name)

            surface.blit(self.icon, (15, (self.height - self.icon.get_height())/2))
            surface.blit(font.render(self.name, True, 0x5f5f5fff), (35, (self.height - size[1])/2))

    def makeGeneratorsContainer(self) -> Container:
        el = Container(0, 0, 150, self.height - 30)
        el.style.display("grid")

        event = GeneratorsEvent()
        generators: list[Generator] \
                  = event._GeneratorsEvent__generators  # type: ignore
                                                        # retardedahh no support in vs code

        EventManager.fire(event)

        for gen in generators:
            el.addREWidget(NewProjectScreen.GeneratorButton.Builder()
                                                                .kw(name=gen.getName(), icon=gen.getIcon())
                                                                .size(100, 24)
                                                            .build())

        return el

    def makeFormContainer(self) -> Container:
        el = Container(0, 0, self.width - 150, self.height - 30)
        return el

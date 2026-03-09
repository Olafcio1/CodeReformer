import pygame
import os

from ....resources import ResourceManager
from ....util.event import EventManager

from ....lib.TextUtil import TextUtil

from ....lib.screen.Screen import Screen

from ....lib.screen.widget.Container import Container
from ....lib.screen.widget.ClippedWidget import ClippedWidget

from ....util.settings.Setting import Setting
from ....util.settings.set_value.StringValue import StringValue
from ....util.settings.set_value.PickValue import PickValue

from ...settings import widget as SeWidget

from .Generator import Generator
from .GeneratorsEvent import GeneratorsEvent, GeneratorType

from typing import Callable

class NewProjectScreen(Screen):
    gensEl: Container
    formEl: Container

    def init(self) -> None:
        window = Container()
        window.style.display("grid")
        window.style.background(0x333433)

        titlebar = Container(0, 0, self.width, 30)
        titlebar.style.borderBottom(0x222322)
        titlebar.text = ("New Project", 0xcfcfcfff, ResourceManager.font["/font/LEXEND.TTF"])

        content = Container(0, 30, self.width, self.height - 30)
        content.style.display("flex")

        content.addREWidget(gensEl := self.__makeGeneratorsContainer())
        content.addREWidget(formEl := self.__makeFormContainer())

        self.gensEl = gensEl
        self.formEl = formEl

        window.addREWidget(titlebar)
        window.addREWidget(content)

        self.addREWidget(window)

    class GeneratorButton(ClippedWidget):
        name: str
        icon: pygame.Surface

        onClick: Callable[[], None]

        def __init__(
                self,
                x: int, y: int,
                width: int, height: int,
                *,
                generator: GeneratorType,
                nps: "NewProjectScreen"
        ):
            super().__init__(x, y, width, height)

            self.name = generator.getName()
            self.icon = pygame.transform.smoothscale(generator.getIcon(), (min(25, self.height - 5), min(25, self.height - 5)))

            self.onClick = lambda: nps.setGenerator(generator())

        def renderClipped(self, surface: pygame.Surface) -> None:
            font = ResourceManager.font['/font/LEXEND.TTF']
            size = font.size(self.name)

            if self.isHovered():
                surface.fill(0x393a39)

            surface.blit(self.icon, (15, (self.height - self.icon.get_height())/2))
            surface.blit(font.render(self.name, True, 0x5f5f5fff), (40, (self.height - size[1])/2))

        def mousePressed(self, x: int, y: int, button: int) -> None:
            if self.isHovered():
                super().mousePressed(x, y, button)
                self.onClick()

    class ContentTitle(ClippedWidget):
        text: str

        def __init__(
                self,
                x: int, y: int,
                width: int, height: int,
                *,
                text: str
        ):
            super().__init__(x, y, width, height)
            self.text = text

        def renderClipped(self, surface: pygame.Surface) -> None:
            font = ResourceManager.font['/font/LEXEND.TTF']
            font.set_bold(True)

            surface.blit(pygame.transform.smoothscale_by(
                font.render(self.text.upper(), True, 0xacacacff),
                .8
            ), (0, 0))

            font.set_bold(False)

    def setGenerator(self, generator: Generator) -> None:
        self.formEl.clear()
        self.formEl.addREWidget(NewProjectScreen.ContentTitle \
                                                .Builder() \
                                                    .kw(text=generator.getName())
                                                    .size(self.formEl.innerWidth, 20)
                                                .build())

        baseSettings: list[Setting] = [
            SName := Setting(
                name="Name",
                value=StringValue("")
            ),
            SPath := Setting(
                name="Path",
                value=StringValue("~/CodeReformerProjects")
            )
        ]

        self.appendSettings(baseSettings)

        categories = generator.getCategories()

        for category in categories.values():
            self.formEl.addREWidget(NewProjectScreen.ContentTitle \
                                                    .Builder() \
                                                        .kw(text=category.name)
                                                        .size(self.formEl.innerWidth, 20)
                                                    .build()
                                                    .style("""
                                                           margin_top: 5
                                                           """))

            self.appendSettings([*category.settings.values()])

        createBtn = Container(
                        -1, -1,
                        150, 30
                    ).setText("Create", 0xcfcfcfff, ResourceManager.font['/font/LEXEND.TTF']) \
                     .style("""
                            background: 0x0e477e
                            border: 0x222322, 0x222322, 0x222322, 0x222322
                            margin_top: 5
                            """)

        def onClick(x, y, button):
            nonlocal createBtn
            if createBtn.isHovered(x, y):
                generator.create(os.path.expanduser(SPath.value.value) + "/" + SName.value.value)

        createBtn.mousePressed = onClick
        self.formEl.addREWidget(createBtn)

    def appendSettings(self, settings: list[Setting]) -> None:
        font = ResourceManager.font['/font/LEXEND.TTF']
        valueX = max([TextUtil.size(setting.name, font)[0] for setting in settings])

        for setting in settings:
            self.formEl.addREWidget(
                {
                    StringValue: SeWidget.TextInput,
                    PickValue: SeWidget.PickSelect
                }[type(setting.value)] \
                                       .Builder()
                                           .kw(setting=setting, valueX=valueX)
                                           .size(350, 20)
                                       .build())

    def __makeGeneratorsContainer(self) -> Container:
        el = Container(0, 0, 150, self.height - 30)
        el.style.display("grid")
        el.style.borderRight(0x222322)

        event = GeneratorsEvent()
        generators: list[GeneratorType] \
                  = event._GeneratorsEvent__generators  # type: ignore
                                                        # retardedahh no support in vs code

        EventManager.fire(event)

        for gen in generators:
            el.addREWidget(NewProjectScreen.GeneratorButton \
                                           .Builder()
                                               .kw(generator=gen, nps=self)
                                               .size(el.width, 34)
                                           .build()
                                           .style("""
                                                  border_bottom: 0x222322
                                                  """))

        return el

    def __makeFormContainer(self) -> Container:
        el = Container(0, 0, self.width - 150, self.height - 30)
        el.style.display("grid")
        el.style.paddingTop(8)
        el.style.paddingLeft(8)
        el.style.gap(8)

        return el

import pygame
import math
import os

from ...lib.screen.Screen import Screen
from ...lib.screen.widget.ClippedWidget import ClippedWidget
from ...lib.screen.widget.Container import Container, Text
from ...lib.screen.widget.Widget import Widget

from ...resources import ResourceManager

from typing import Callable

class ProjectScreen(Screen):
    class Background(Widget):
        def renderWidget(self, surface: pygame.Surface) -> None:
            surface.fill(0x333433)

    class Explorer(Container):
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

        class FolderArrow(ClippedWidget):
            right: int
            listener: ...

            def __init__(self, *args, right: int, listener: ..., **kwargs):
                super().__init__(*args, **kwargs)

                self.right = right
                self.listener = listener

            @staticmethod
            def quintic(num: float) -> float:
                return 1 - ((1 - num) ** 5)

            def renderClipped(self, surface: pygame.Surface) -> None:
                size = min(self.height, self.width)

                x = self.width  - size - self.right
                y = self.height - size

                if self.listener.is_open():
                    y -= 2

                    pygame.draw.lines(surface, 0x777877, closed=False, points=[
                        (x + size/4,    y + size/2),
                        (x + size/2,    y + size/1.25),
                        (x + size/1.25, y + size/2)
                    ])
                else:
                    pygame.draw.lines(surface, 0x777877, closed=False, points=[
                        (x + size/2,    y + size/4),
                        (x + size/1.25, y + size/2),
                        (x + size/2,    y + size/1.25)
                    ])

        path: str

        def __init__(self, path: str, /, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.path = path

            self.style.background(0x333433)
            self.style.border((0x555655, 0x555655, 0x555655, 0x555655))
            self.style.paddingTop(8)
            self.style.gap(4)
            self.style.display("grid")

            self.extractFolder(self.path, self)

        def extractFolder(cls, path: str, self: Container) -> None:
            files = os.listdir(path)

            for fn in files:
                file = Container(self.innerWidth, 16 + (7*2))

                file.style.display("flex")
                file.style.gap(7)
                file.style.padding((7, 7, 7, 7))

                file.style_hover.background(0x444544)

                fp = path + "/" + fn

                if isdir := os.path.isdir(fp):
                    file.addREWidget(type(cls).FolderIcon.Builder() \
                                                            .pos(0, 0) \
                                                            .size(16, 16) \
                                                          .build())

                    class Listener:
                        path: str
                        file: Container

                        def __init__(self, path: str, file: Container):
                            self.path = path
                            self.file = file

                        contents: Container|None = None

                        def is_open(self) -> bool:
                            return self.contents is not None

                        def mousedown(self, _):
                            if self.is_open():
                                self.contents.remove()
                                self.contents = None

                                return

                            self.contents = cls.openFolder(self.path, self.file)

                    file.on("mousedown", (listener := Listener(fp, file)).mousedown)
                else:
                    # TODO Support custom file icons.
                    #      Through resources or methods?

                    file.addREWidget(type(cls).FileIcon.Builder() \
                                                          .pos(0, 0) \
                                                          .size(16, 16) \
                                                        .build())

                file.text += Text(
                    text  = fn,
                    color = 0x8f8f8fff,
                    font  = ResourceManager.font["/font/LEXEND.TTF"],
                    align = "left"
                )

                file.child(1).style.marginTop(-2)

                if isdir:
                    # TODO Move this math to a new field, 'Styleable#availableWidth'
                    file.addREWidget(type(cls).FolderArrow.Builder() \
                                                            .size(file.innerWidth - 7 - file.child(0).width - file.child(1).width, 16) \
                                                            .kw(right=15, listener=listener)
                                                          .build())

                self.addREWidget(file)

        def openFolder(self, path: str, file: Container) -> Container:
            padX = 6

            content = Container(file.parent.innerWidth, 0)
            content.style.paddingLeft(padX)
            content.style.display("grid")
            content.style.gap(7)
            content.style.marginTop(2)
            content.style.marginBottom(2)
            content.layout.dynamicHeight(True)

            self.extractFolder(path, content)

            file.after(content)

            return content

    baseDir: str

    def __init__(self, baseDir: str):
        super().__init__()

        self.baseDir = baseDir

    def init(self) -> None:
        self.addRenderable(ProjectScreen.Background())
        self.addREWidget(ProjectScreen.Explorer(self.baseDir, x=10, y=10, \
                                                              width=160, height=self.height - 20))

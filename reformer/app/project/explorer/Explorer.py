import pygame
import os

from .icon.FileIcon import FileIcon
from .icon.FolderIcon import FolderIcon
from .icon.FolderArrow import FolderArrow

from .FileOpenEvent import FileOpenEvent

from ....lib.screen.widget.Container import Container, Text
from ....resources import ResourceManager
from ....common import invoker

from typing import Callable

class Explorer(Container):
    path: str

    def __init__(self, path: str, /, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.path = path

        self.style.background(0x333433)
        self.style.border((0x555655, 0x555655, 0x555655, 0x555655))
        self.style.paddingTop(8)
        self.style.gap(4)
        self.style.display("grid")

        self.map("fileopen", FileOpenEvent)
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
                file.addREWidget(FolderIcon.Builder() \
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

                file.addREWidget(FileIcon.Builder() \
                                            .pos(0, 0) \
                                            .size(16, 16) \
                                         .build())

                file.on("mousedown", invoker(
                    lambda _, event: cls.fire(event),
                    FileOpenEvent(fp, file)
                ))

            file.text += Text(
                text  = fn,
                color = 0x8f8f8fff,
                font  = ResourceManager.font["/font/LEXEND.TTF"],
                align = "left"
            )

            file.child(1).style.marginTop(-2)

            if isdir:
                # TODO Move this math to a new field, 'Styleable#availableWidth'
                file.addREWidget(FolderArrow.Builder() \
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

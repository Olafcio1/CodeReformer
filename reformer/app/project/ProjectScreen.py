import pygame

from typing import Callable

from .explorer.Explorer import Explorer
from .explorer.FileOpenEvent import FileOpenEvent

from .code.Code import Code

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

    explorer: Explorer
    code: Code

    def init(self) -> None:
        self.addRenderable(ProjectScreen.Background())
        self.addREWidget(explorer := Explorer(self.baseDir, x=10, y=10, \
                                                            width=160, height=self.height - 20))
        self.addREWidget(code := Code(x=160 + 10 + 10, y=10, \
                                      width=self.width - 180 - 10, height=self.height - 20))

        self.explorer = explorer
        self.code = code

        explorer.on("fileopen", self.openFile)

    decoder: Callable[[bytes], str]
    encoder: Callable[[str], bytes]
    encoding: str

    def openFile(self, event: FileOpenEvent) -> None:
        with open(event.path, "rb") as f:
            data = f.read()

            if data.startswith(b'\xef\xbb\xbf'):
                self.encoder = lambda content: b'\xef\xbb\xbf' + content.encode("utf-8", errors="surrogatepass")
                self.decoder = lambda content: content.removeprefix(b'\xef\xbb\xbf').decode("utf-8", errors="surrogatepass")
                self.encoding = "UTF-8 with BOM"
            else:
                self.encoder = lambda content: content.encode("utf-8", errors="surrogatepass")
                self.decoder = lambda content: content.decode("utf-8", errors="surrogatepass")
                self.encoding = "UTF-8"

            self.code.lines = self.decoder(data).splitlines()
            self.code.forceRender()

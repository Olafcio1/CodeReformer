import pygame
from typing import Protocol

class IRenderable(Protocol):
    ## LAYOUT ##
    def lay(self) -> None:
        ...

    ## RENDERING ##
    def render(self, surface: pygame.Surface) -> None:
        ...

    def renderChanged(self, surface: pygame.Surface) -> None:
        ...

    ## PENDING RERENDER ##
    def pendingRerender(self) -> bool:
        ...

    def anyChanged(self) -> bool:
        ...

    def refreshTime(self) -> int|None:
        ...

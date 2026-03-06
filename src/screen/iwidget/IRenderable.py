import pygame
from typing import Protocol

class IRenderable(Protocol):
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

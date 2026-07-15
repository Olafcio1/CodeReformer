import pygame
from typing import TypedDict, NotRequired, Literal

class Text(TypedDict):
    text: str
    color: int
    font: pygame.font.Font
    align: NotRequired[Literal["left"] | Literal["center"]]

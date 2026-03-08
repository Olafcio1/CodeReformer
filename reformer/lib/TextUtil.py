import pygame
from typing import final

@final
class TextUtil:
    def __init__(self):
        raise Exception("Initialization not permitted")

    @staticmethod
    def size(text: str, font: pygame.font.Font) -> tuple[int, int]:
        return font.render(text, True, 0x000000ff).get_size()

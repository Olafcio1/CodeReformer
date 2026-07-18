import pygame
import os

from typing import ClassVar
from .logger import *

class ResourceManager:
    image: ClassVar[dict[str, pygame.Surface]] = {}
    font: ClassVar[dict[str, pygame.font.Font]] = {}

    @classmethod
    def loadBuiltin(cls, *, rel: str = ""):
        cls.load("assets" + rel)

    @classmethod
    def load(cls, path: str, *, rel: str = ""):
        files = os.listdir(path)

        for fn in files:
            sub = path + "/" + fn
            subRel = rel + "/" + fn

            if os.path.islink(sub):
                getlogger() << ("[WARN] Blocked link %r" % sub)
            elif os.path.isfile(sub):
                if fn.lower().endswith((".jpg", ".jpeg", ".png")):
                    cls.image[subRel] = pygame.image.load(sub)
                elif fn.lower().endswith((".ttf", ".otf")):
                    cls.font[subRel] = pygame.font.Font(sub, 16)
                    cls.font[subRel + ":-1"] = pygame.font.Font(sub, 15)
                    cls.font[subRel + ":-2"] = pygame.font.Font(sub, 14)
                else:
                    getlogger() << ("[WARN] Unrecognized file %r" % sub)
            elif os.path.isdir(sub):
                cls.load(sub, rel=subRel)
            else:
                getlogger() << ("[WARN] Non-standard file %r" % sub)

import os

from .PluginLoader import PluginLoader
from typing import final

@final
class PluginScanner:
    def __init__(self):
        raise Exception("Initialization not permitted")

    @staticmethod
    def scan(folder: str) -> None:
        files = os.listdir(folder)
        for fn in files:
            sub = folder + "/" + fn
            if os.path.isdir(sub) and os.path.isfile(sub + "/reformer.jsonc"):
                PluginLoader(sub).load()

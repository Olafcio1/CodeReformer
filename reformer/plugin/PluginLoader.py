import json
import sys
import os

from .PluginManifest import PluginManifest

class PluginLoader:
    path: str
    manifest: PluginManifest

    __package: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.manifest = self.getManifest()

        split = path.replace('\\', '/').split('/')

        self.__package = split.pop() + '.' + \
                          split.pop()

        parent = '/'.join(split)
        if parent not in sys.path:
            sys.path.insert(1, parent)

    def load(self) -> None:
        for script in self.manifest.scripts:
            path = script.value

            assert path.endswith(".py")

            __import__(self.__package + os.path.normpath(path.removesuffix('.py')) \
                                            .replace('\\', '/')
                                            .replace('/', '.'))

    def getManifest(self) -> PluginManifest:
        with open(self.path + "/reformer.jsonc") as f:
            data = json.load(f)

        return PluginManifest(data)

import json
import sys
import os

from .PluginManifest import PluginManifest

from ..util.event import EventManager
from ..packs import Pack

class PluginLoader:
    path: str
    manifest: PluginManifest

    __package: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.manifest = self.getManifest()

        split = path.replace('\\', '/').split('/')

        self.__package = split.pop(-2) + '.' + \
                         split.pop()

        parent = '/'.join(split)
        if parent not in sys.path:
            sys.path.insert(1, parent)

    def load(self) -> None:
        self.loadAssets()
        self.loadScripts()

    def loadAssets(self) -> None:
        for res in self.manifest.resources:
            path = self.__package.replace('.', '/') + "/" + \
                                                      os.path.normpath(res)

            pack = Pack(path, mergedDefaults={
                "name": self.manifest.name,
                "description": self.manifest.description
            })

            pack.load()

    def loadScripts(self) -> None:
        for script in self.manifest.scripts:
            path = script.value

            assert path.endswith(".py")

            package = self.__package + "." + os.path.normpath(path.removesuffix('.py')) \
                                                .replace('\\', '/') \
                                                .replace('/', '.')

            module = __import__(package)
            names = package.split(".")[1:]

            for name in names:
                module = getattr(module, name)

            clazz = getattr(module, "Plugin")
            inst = clazz()

            EventManager.register(inst)

    def getManifest(self) -> PluginManifest:
        with open(self.path + "/reformer.jsonc") as f:
            raw = f.read()

        lines = filter(lambda line: not line.strip().startswith("//"), raw.splitlines())
        data = json.loads("\n".join(lines))

        return PluginManifest(data)

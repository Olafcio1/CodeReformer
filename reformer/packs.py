from typing import ClassVar, Any
from .resources import ResourceManager

class Pack:
    __path: str

    def __init__(self, path: str, *, mergedDefaults: dict[str, Any] = {}) -> None:
        self.__path = path

        with open(path + "/pack.properties", "r", encoding="utf-8") as f:
            raw = f.read().splitlines()

        properties = {}
        for line in raw:
            key, _, value = line.partition("=")
            properties[key.strip()] = value.strip()

        self.merged   = properties.get("merged", False)
        self.required = properties.get("required", self.merged)
        self.default  = properties.get("default", self.required)

        if self.merged:
            for key in mergedDefaults:
                if key not in type(self).__annotations__:
                    print("[Pack/ERROR] Cannot set undefined property %r (from merged defaults)" % key)
                elif key not in properties:
                    setattr(self, key, mergedDefaults[key])

        if 'name' in properties:
            self.name = properties['name']

        if 'description' in properties:
            self.description = properties.get("description", "")

        for key in properties:
            if key not in ("merged", "required", "default", "name", "description"):
                print("[Pack/ERROR] Cannot set undefined property %r" % key)

    name: str
    description: str

    merged: bool
    default: bool
    required: bool

    def load(self) -> None:
        ResourceManager.load(self.__path)
        PackManager.loadedPacks.append(self)

class PackManager:
    loadedPacks: ClassVar[list[Pack]] = []
    availablePacks: ClassVar[list[Pack]] = []

    @classmethod
    def addPack(cls, pack: Pack) -> None:
        cls.availablePacks.append(pack)

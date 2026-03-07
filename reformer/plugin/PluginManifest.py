from typing import Literal, Any

class PluginManifest:
    class Script:
        type: Literal["plugin"]
        value: str

        def __init__(self, data: dict[str, Any]) -> None:
            self.type = data['type']
            self.value = data['value']

            assert self.type in ("plugin",)

    name: str
    version: int
    version_name: str
    description: str
    scripts: list[Script]

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data['name']
        self.version = data['version']
        self.version_name = data['version_name']
        self.description = data['description']
        self.scripts = [PluginManifest.Script(obj) for obj in data['scripts']]

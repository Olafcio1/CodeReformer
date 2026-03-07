from ...src.event.EventHandler import EventHandler
from ...src.home.new_project.GeneratorsEvent import GeneratorsEvent

from .javagen import JavaGenerator

class Plugin:
    @EventHandler
    def onGenerators(self, event: GeneratorsEvent) -> None:
        event.add(JavaGenerator())

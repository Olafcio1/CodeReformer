from reformer.util.event.EventHandler import EventHandler
from reformer.app.home.new_project.GeneratorsEvent import GeneratorsEvent

from .phpgen import PHPGenerator

class Plugin:
    @EventHandler
    def onGenerators(self, event: GeneratorsEvent) -> None:
        event.add(PHPGenerator)

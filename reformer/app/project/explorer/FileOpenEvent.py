from typing import Final

from ....lib.screen.widget.Container import Container
from ....util.event import Event

class FileOpenEvent(Event):
	path:    Final[str]
	element: Final[Container]

	def __init__(self, path: str, element: Container):
		self.path = path
		self.element = element

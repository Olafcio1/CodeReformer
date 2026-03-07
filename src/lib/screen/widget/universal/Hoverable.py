from abc import ABCMeta
from ...iwidget.IWidget import IWidget

class Hoverable(IWidget, metaclass=ABCMeta):
    def isHovered(self, x: int, y: int) -> bool:
        return x >= self.x and y >= self.y and x < self.x + self.width and y < self.y + self.height

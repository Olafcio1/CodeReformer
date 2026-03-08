from abc import ABCMeta

from .universal.Hoverable import Hoverable
from ..iwidget.IAttacher import IAttacher

class Attacher(IAttacher, metaclass=ABCMeta):
    __interacted: bool
    __unhovered: bool

    def __init__(self) -> None:
        self.__interacted = False
        self.__unhovered = False

    ###########
    ## MOUSE ##
    ###########

    def mouseMoved(self, x: int, y: int) -> None:
        super().mouseMoved(x, y)  # type: ignore

        if type(self).mouseMoved == Attacher.mouseMoved:
            if (
                    isinstance(self, Hoverable) and
                    self._Hoverable__usesHover  # type: ignore
            ):
                if self.isHovered(x, y):
                    self.__unhovered = False
                elif not self.__unhovered:
                    self.__unhovered = True
                else: return
            else: return

        self.__interacted = True

    def mousePressed(self, x: int, y: int, button: int) -> None:
        super().mousePressed(x, y, button)  # type: ignore

        if type(self).mousePressed != Attacher.mousePressed:
            self.__interacted = True

    def mouseReleased(self, x: int, y: int, button: int) -> None:
        super().mouseReleased(x, y, button)  # type: ignore

        if type(self).mouseReleased != Attacher.mouseReleased:
            self.__interacted = True

    ##############
    ## KEYBOARD ##
    ##############

    def keyPressed(self, key: int, unicode: str) -> None:
        super().keyPressed(key, unicode)  # type: ignore

        if type(self).keyPressed != Attacher.keyPressed:
            self.__interacted = True

    def keyReleased(self, key: int, unicode: str) -> None:
        super().keyReleased(key, unicode)  # type: ignore

        if type(self).keyReleased != Attacher.keyReleased:
            self.__interacted = True

    ###########
    ## STATE ##
    ###########

    def _interacted(self) -> bool:
        return self.__interacted

    def _reset(self) -> None:
        self.__interacted = False

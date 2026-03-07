from abc import ABCMeta
from ..iwidget.IAttacher import IAttacher

class Attacher(IAttacher, metaclass=ABCMeta):
    __interacted: bool

    def __init__(self) -> None:
        self.__interacted = False

    ###########
    ## MOUSE ##
    ###########

    def mouseMoved(self, x: int, y: int) -> None:
        self.__interacted = True

    def mousePressed(self, x: int, y: int, button: int) -> None:
        self.__interacted = True

    def mouseReleased(self, x: int, y: int, button: int) -> None:
        self.__interacted = True

    ##############
    ## KEYBOARD ##
    ##############

    def keyPressed(self, key: int, unicode: str) -> None:
        self.__interacted = True

    def keyReleased(self, key: int, unicode: str) -> None:
        self.__interacted = True

    ###########
    ## STATE ##
    ###########

    def _interacted(self) -> bool:
        return self.__interacted

    def _reset(self) -> None:
        self.__interacted = False

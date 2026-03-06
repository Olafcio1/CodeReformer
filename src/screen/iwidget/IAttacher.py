from typing import Protocol

class IAttacher(Protocol):
    ###########
    ## MOUSE ##
    ###########

    def mouseMoved(self, x: int, y: int) -> None:
        ...

    def mousePressed(self, x: int, y: int, button: int) -> None:
        ...

    def mouseReleased(self, x: int, y: int, button: int) -> None:
        ...

    ##############
    ## KEYBOARD ##
    ##############

    def keyPressed(self, key: int, unicode: str) -> None:
        ...

    def keyReleased(self, key: int, unicode: str) -> None:
        ...

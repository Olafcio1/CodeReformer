from typing import TypeVarTuple, Protocol
from ...iwidget.IWidget import IWidget

Args = TypeVarTuple('Args')

class AWidget(IWidget, Protocol[*Args]):
    x: int
    y: int

    width: int
    height: int

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            *args: *Args
    ) -> None:
        ...

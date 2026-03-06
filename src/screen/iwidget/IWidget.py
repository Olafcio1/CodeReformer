from .IAttacher import IAttacher
from .IRenderable import IRenderable

from typing import TypeVarTuple, Protocol

Args = TypeVarTuple('Args')

class IWidget(IAttacher, IRenderable, Protocol[*Args]):
    x: int
    y: int

    width: int
    height: int

    parent: "IWidget | None"

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            *args: *Args
    ) -> None:
        ...

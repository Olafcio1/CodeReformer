from typing import Protocol

from .IWidget import IWidget
from .IAttacher import IAttacher
from .IRenderable import IRenderable

class IContainer(IWidget, Protocol):
    x: int
    y: int

    width: int
    height: int

    _attachers: list[IAttacher]
    _renderables: list[IRenderable]

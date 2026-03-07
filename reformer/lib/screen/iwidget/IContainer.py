from typing import Protocol

from .IWidget import IWidget
from .IAttacher import IAttacher
from .IRenderable import IRenderable

class IContainer(IWidget, Protocol):
    _widgets: list[IWidget]
    _attachers: list[IAttacher]
    _renderables: list[IRenderable]

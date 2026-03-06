from .IAttacher import IAttacher
from .IRenderable import IRenderable

from typing import Protocol

class IWidget(IAttacher, IRenderable, Protocol):
    pass

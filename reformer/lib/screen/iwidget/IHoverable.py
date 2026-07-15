from typing import Protocol

class IHoverable(Protocol):
    def isHovered(self) -> bool:
        ...

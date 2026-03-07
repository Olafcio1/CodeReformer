from typing import Callable, TypeVar
from ..Event import Event

T = TypeVar('T', bound="Event", covariant=True)
EventTarget = Callable[[T], None] | object

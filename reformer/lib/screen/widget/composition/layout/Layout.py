from ..Backable import Backable, T

from ..CallSetter import CallSetter
from ..CallLogger import CallLogger

from .key import StDynamicHeight as keymod

from .key.StDynamicHeight import StDynamicHeight

from abc import ABCMeta
from typing import Generic

class Layout(
        Backable[T],
        CallSetter[T],
        Generic[T],

        CallLogger,

        StDynamicHeight,

        metaclass=ABCMeta
):
    def __init__(self, arg):
        Backable.__init__(self, arg)
        CallLogger.__init__(self, keymod)

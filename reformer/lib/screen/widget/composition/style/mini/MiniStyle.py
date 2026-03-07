from ...Backable import Backable, T
from ..CallSetter import CallSetter

from ..key.StBackground import StBackground
from ..key.StBorder import StBorder

from abc import ABCMeta
from typing import Generic

class MiniStyle(
        Backable[T],
        CallSetter[T],
        Generic[T],

        StBackground,
        StBorder,

        metaclass=ABCMeta
): pass

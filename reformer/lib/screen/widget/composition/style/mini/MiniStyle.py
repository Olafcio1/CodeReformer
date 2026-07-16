from ...Backable import Backable, T

from ...CallSetter import CallSetter
from ...CallLogger import CallLogger

from ..key import StBackground as keymod

from ..key.StBackground import StBackground
from ..key.StBorder import StBorder
from ..key.StMargin import StMargin

from abc import ABCMeta
from typing import Generic

class MiniStyle(
        Backable[T],
        CallSetter[T],
        Generic[T],

        CallLogger,

        StBackground,
        StBorder,
        StMargin,

        metaclass=ABCMeta
):
    def __init__(self, arg):
        Backable.__init__(self, arg)
        CallLogger.__init__(self, keymod)

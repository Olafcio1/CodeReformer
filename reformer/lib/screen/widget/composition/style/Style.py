from ..Backable import Backable, T
from .CallSetter import CallSetter

from .key.StPadding import StPadding
from .key.StDisplay import StDisplay
from .key.StGap import StGap
from .key.StBackground import StBackground
from .key.StBorder import StBorder
from .key.StMargin import StMargin

from abc import ABCMeta
from typing import Generic

class Style(
        Backable[T],
        CallSetter[T],
        Generic[T],

        StPadding,
        StDisplay,
        StGap,
        StBackground,
        StBorder,
        StMargin,

        metaclass=ABCMeta
): pass

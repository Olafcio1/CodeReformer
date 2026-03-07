from ..Backable import Backable, T

from .key.StPadding import StPadding
from .key.StDisplay import StDisplay
from .key.StGap import StGap
from .key.StBackground import StBackground
from .key.StBorder import StBorder

from abc import ABCMeta
from typing import Generic

class Style(
        Backable[T],
        Generic[T],

        StPadding,
        StDisplay,
        StGap,
        StBackground,
        StBorder,

        metaclass=ABCMeta
): pass

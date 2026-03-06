from ..Backable import Backable, T

from .key.StPadding import StPadding
from .key.StDisplay import StDisplay
from .key.StGap import StGap

from abc import ABCMeta
from typing import Generic

class Style(
        Backable,
        Generic[T],

        StPadding,
        StDisplay,
        StGap,

        metaclass=ABCMeta
): pass

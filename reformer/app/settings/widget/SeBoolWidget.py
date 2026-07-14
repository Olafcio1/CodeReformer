import pygame

from ..SettingWidget import SettingWidget

from ....lib.TextUtil import TextUtil
from ....lib.FigureUtil import FigureUtil

from ....resources import ResourceManager
from ....util.settings.set_value.PickValue import PickValue

from typing import Final

class SeBoolWidget(SettingWidget[PickValue]):
    """
    Bool checkbox widget.

    :api-status: experimental
    """

    def renderWidget(self, surface: pygame.Surface) -> None:
        super().renderWidget(surface)

        x = self.x + self.valueX - 5
        y = self.y

        w = \
        h = min(self.width, self.height)

        FigureUtil.roundedRect_fill(surface, 0x4d4d4d if self.value.value else 0x2c2c2c, (x, y, w, h))
        FigureUtil.roundedRect_stroke(surface, 0x4d4d4d, (x, y, w, h))

        if self.value.value:
            # Checkmark
            pygame.draw.line(surface, 0x2c2c2c, (x + w/4, y + h/2.5 + 3), (x + w/2, y + h/2 + 3))
            pygame.draw.line(surface, 0x2c2c2c, (x + w/1.35, y + h/6 + 3), (x + w/2, y + h/2 + 3))

    ###########
    ## MOUSE ##
    ###########

    def mouseIn(self, x: int, y: int) -> None:
        self.value.value = not self.value.value

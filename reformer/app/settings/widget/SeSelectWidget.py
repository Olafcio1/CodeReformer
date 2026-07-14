import pygame

from ..SettingWidget import SettingWidget

from ....lib.TextUtil import TextUtil
from ....lib.FigureUtil import FigureUtil

from ....resources import ResourceManager
from ....util.settings.set_value.SelectValue import SelectValue

from typing import Final

class SeSelectWidget(SettingWidget[SelectValue]):
    """
    Select dropdown widget.

    :api-status: experimental
    """

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            *,
            setting: SelectValue,
            valueX: int
    ):
        super().__init__(x, y, width, height, setting=setting, valueX=valueX)

        self._font = ResourceManager.font['/font/LEXEND.TTF:-2']

    def renderWidget(self, surface: pygame.Surface) -> None:
        super().renderWidget(surface)

        x = self.x + self.valueX - 5
        y = self.y

        options = self.value.options
        text = self.value.value

        size = TextUtil.size(text, self._font)
        image = self._font.render(text, True, 0xa2a2a2ff)

        FigureUtil.roundedRect_fill  (surface, 0x2c2c2c, (x, y - 3, size[0] + 12, self.height + 6))
        FigureUtil.roundedRect_stroke(surface, 0x4d4d4d, (x, y - 3, size[0] + 12, self.height + 6))

        surface.blit(image, (x + 6, y + (self.height - size[1])/2))

    ###########
    ## MOUSE ##
    ###########

    def mouseIn(self, x: int, y: int) -> None:
        ...

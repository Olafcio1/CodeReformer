import pygame

from ..SettingWidget import SettingWidget

from ....lib.TextUtil import TextUtil
from ....lib.FigureUtil import FigureUtil

from ....resources import ResourceManager
from ....util.settings.set_value.PickValue import PickValue

from typing import Final

class SePickWidget(SettingWidget[PickValue]):
    """
    Pick input widget.

    :api-status: experimental
    """

    def renderWidget(self, surface: pygame.Surface) -> None:
        super().renderWidget(surface)

        options = self.value.options

        block_padding: Final = 5
        xpadding:      Final = 2
        ypadding:      Final = 3
        gap:           Final = 2

        x = self.x + self.valueX - 5
        w = sum([TextUtil.size(opt, self._font)[0] + \
                 block_padding*2 + \
                 gap

                 for opt in options]
        ) - gap \
          + xpadding*2

        yA = self.y - ypadding
        hA = self.height + ypadding*2

        FigureUtil.roundedRect_fill(surface, 0x2c2c2c, (x, yA, w, hA))
        FigureUtil.roundedRect_stroke(surface, 0x4d4d4d, (x, yA, w, hA))

        y = self.y
        h = self.height

        for i, opt in enumerate(options):
            x += block_padding

            text = str(opt)
            size = TextUtil.size(text, self._font)

            if (i+1)%2 == 0:
                FigureUtil.roundedRect_fill(surface, 0x3c3c3c, (x, y, block_padding*2 + size[0], h))

            size = TextUtil.size(text, self._font)
            image = self._font.render(text, True, 0xa2a2a2ff)

            surface.blit(image, (x + (block_padding), y + (h - size[1])/2))

            x += size[0]
            x += gap

    ###########
    ## MOUSE ##
    ###########

    def mouseIn(self, x: int, y: int) -> None:
        ...

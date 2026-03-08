import pygame

from ..SettingWidget import SettingWidget

from ....resources import ResourceManager
from ....util.settings.set_value.StringValue import StringValue

class SeTextWidget(SettingWidget[StringValue]):
    """
    Text input widget.<br/>
    TODO: please fix ts!

    :api-status: experimental
    """

    __position: int

    __charX: list[int]
    __currentX: int

    def init(self):
        self.__position = -1

        self.__charX = [self.__textSize(ch)[0] for ch in self.value.value]
        self.__currentX = -1

    def __textSize(self, text: str) -> tuple[int, int]:
        return self._font.render(text, True, 0x000000ff).get_size()

    def renderWidget(self, surface: pygame.Surface) -> None:
        super().renderWidget(surface)

        self.__roundedRect(surface, 0xb2b2b2, (self.x + self.valueX - 5, self.y - 1, self.width + 4, self.height + 3))

        surface.blit(self._font.render(self.value.value, True, 0xa2a2a2ff), (self.x + self.valueX, self.y))
        surface.fill(0x555555, (self.x + self.valueX + self.__currentX, self.y, 2, self.height))

    def __roundedRect(self, surface: pygame.Surface, color: int, pos: tuple[int, int, int, int]) -> None:
        pygame.draw.rect(surface, color, pos, 1)

        x, y, w, h = pos

        for i in range(3):
            # Left-Top
            surface.set_at((x + i, y), 0x333433)
            surface.set_at((x, y + i), 0x333433)

            surface.set_at((x + (3 - i), y + i), 0xb2b2b2)

            # Right-Bottom
            surface.set_at((x + w - 1 - i, y + h - 1), 0x333433)
            surface.set_at((x + w - 1, y + h - 1 - i), 0x333433)

            surface.set_at((x + w - 1 - i, y + h - (3 - i + 1)), 0xb2b2b2)

    ###########
    ## MOUSE ##
    ###########

    def mouseIn(self, x: int, y: int) -> None:
        self.__position = 0
        self.__currentX = 0

        diff = x - self.x
        forX = 0

        for i, w in enumerate(self.__charX):
            right = forX + w

            if diff <= right:
                mid = forX + (w/2)

                if diff < mid:
                    # closer to left
                    self.__position = i
                    self.__currentX = forX
                else:
                    # closer to right
                    self.__position = i + 1
                    self.__currentX = right

                return

            forX = right

        self.__position = len(self.__charX)
        self.__currentX = forX-w

    def mouseOut(self) -> None:
        self.__position = -1

    ##############
    ## KEYBOARD ##
    ##############

    def keyPressed(self, key: int, unicode: str) -> None:
        if self.isFocused():
            print("[TextInput] [Keyboard] %s" % key)
            if key == pygame.K_LEFT:
                if self.__position > 0:
                    self.__currentX -= self.__charX[self.__position - 1]
                    self.__position -= 1
            elif key == pygame.K_RIGHT:
                if self.__position < len(self.value.value):
                    self.__currentX += self.__charX[self.__position]
                    self.__position += 1
            elif key == pygame.K_HOME:
                self.__position = 0
                self.__currentX = 0
            elif key == pygame.K_END:
                self.__position = len(self.value.value)
                self.__currentX = sum(self.__charX[1:])
            elif unicode == '\x08':
                if self.__position == len(self.value.value)-1:
                    self.value.value = self.value.value[:-1]

                    self.__currentX -= self.__charX.pop()
                    self.__position -= 1
                elif self.__position > 0:
                    self.value.value = self.value.value[:self.__position-1] + self.value.value[self.__position:]

                    self.__position -= 1
                    self.__currentX -= self.__charX.pop(self.__position)
            elif unicode == '\r':
                pass
            elif unicode != '':
                if self.__position == len(self.value.value)-1:
                    self.value.value += unicode
                else:
                    self.value.value = self.value.value[:self.__position] + unicode + self.value.value[self.__position:]

                width = self.__textSize(unicode)[0]

                self.__charX.insert(self.__position + 1, width)
                self.__position += 1
                self.__currentX += width
            else:
                return

            super().keyPressed(key, unicode)

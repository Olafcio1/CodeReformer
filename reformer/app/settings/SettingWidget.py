from pygame import Surface
from pygame.font import Font

from ...util.settings.Setting import Setting, SettingValue
from ...lib.screen.widget.Widget import Widget

from ...resources import ResourceManager

from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, final

V = TypeVar('V', bound="SettingValue")

class SettingWidget(Widget, Generic[V], metaclass=ABCMeta):
    name: str
    value: V

    valueX: int

    _font: Font
    __focused: bool

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            *,
            setting: Setting[V],
            valueX: int
    ):
        super().__init__(x, y, width, height)

        self.name = setting.name
        self.value = setting.value

        self.valueX = valueX + 10

        self._font = ResourceManager.font['/font/LEXEND.TTF']
        self.__focused = False

        self.init()

    def init(self) -> None:
        pass

    @abstractmethod
    def renderWidget(self, surface: Surface) -> None:
        surface.blit(self._font.render(self.name, True, 0xafafafff), (self.x, self.y))

    @final
    def mousePressed(self, x: int, y: int, button: int) -> None:
        x -= self.valueX
        if self.isHovered(x, y):
            super().mousePressed(x, y, button)

            if button == 1:
                self.__focused = True
                self.mouseIn(x, y)
        else:
            self.__focused = False
            self.mouseOut()

    @abstractmethod
    def mouseIn(self, x: int, y: int) -> None:
        ...

    def mouseOut(self) -> None:
        pass

    def isFocused(self) -> bool:
        return self.__focused

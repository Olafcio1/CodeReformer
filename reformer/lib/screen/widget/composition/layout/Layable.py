from .Layout import Layout
from abc import ABCMeta

class Layable(metaclass=ABCMeta):
    __layout: Layout

    def __init__(self):
        self.__layout = Layout(self)

    @property
    def layout(self):
        return self.__layout

    #########
    ## LAY ##
    #########

    def lay(self):
        if self.layout._dynamicHeight:
            if self.style._display != "grid":
                raise Exception("'dynamic_height' cannot be used with %s 'display' property" % self.style._display)

            prev: IWidget|None = None
            y = self.style._paddingTop

            for element in self._widgets:
                if prev != None:
                    y += self.style._gapVertical

                x = self.style._paddingLeft

                if hasattr(element, 'style'):
                    x += element.style._marginLeft # type: ignore
                    y += element.style._marginTop  # type: ignore

                element.x = x
                element.y = y

                if hasattr(element, 'style'):
                    y += element.style._marginBottom  # type: ignore

                y += element.height
                prev = element

            y += self.style._paddingBottom

            self.height = y

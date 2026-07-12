from abc import ABCMeta
from ...iwidget.IContainer import IContainer

class Parented(metaclass=ABCMeta):
    __self_parent: IContainer|None

    def __init__(self):
        self.__self_parent = None

    @property
    def parent(self):
        return self.__self_parent

    def remove(self):
        parent = self.parent

        if parent is not None:
            parent._renderables.remove(self)
            parent._attachers.remove(self)

            parent._widgets.remove(self)

            parent.forceRender()

from abc import ABCMeta
from ...iwidget.IContainer import IContainer

class Parented(metaclass=ABCMeta):
    __self_parent: IContainer|None

    def __init__(self):
        self.__self_parent = None

    @property
    def parent(self):
        return self.__self_parent

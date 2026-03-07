from abc import ABCMeta
from ...iwidget.IContainer import IContainer

class Parented(metaclass=ABCMeta):
    parent: IContainer|None

    def __init__(self):
        self.parent = None

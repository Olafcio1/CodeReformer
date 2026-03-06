from abc import ABCMeta
from typing import Generic, TypeVar

from ...iwidget.IContainer import IContainer

T = TypeVar('T')

class Backable(Generic[T], metaclass=ABCMeta):
    back: T

    def __init__(self, container: T):
        self.back = container

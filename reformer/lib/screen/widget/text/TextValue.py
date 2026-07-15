from types import EllipsisType as Ellipsis
from typing import overload

from .Text import Text
from .TextWidget import TextWidget

from ...iwidget.IContainer import IContainer

class TextValue(str):
    __parent: IContainer

    def __new__(self, arg: str, /, parent: IContainer):
    	inst = str.__new__(TextValue) if arg is None else str.__new__(TextValue, arg)
    	inst.__parent = parent

    	return inst

    def __init__(self, value: str, /, parent: IContainer):
        ...

    @overload
    def __iadd__(self, args: str) -> "TextValue":
        ...

    @overload
    def __iadd__(self, args: Text) -> Ellipsis:
        ...

    def __iadd__(self, args: str | Text) -> "TextValue | Ellipsis":
        if isinstance(args, str):
            return TextValue(self.__add__(args), parent=self.__parent)
        elif isinstance(args, tuple):
            value, color, font = args
            align = 'center'
        else:
            value = args['text']
            color = args['color']
            font  = args['font']
            align = args.get('align', "center")

        self.__parent.addREWidget(TextWidget(value, color, font, align, \
                                             parent=self.__parent))

        return ...

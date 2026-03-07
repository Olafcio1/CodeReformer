from typing import TypeVar, Callable

T = TypeVar('T', bound="Callable")

def EventHandler(func: T) -> T:
    func.__eventhandler__ = True
    return func

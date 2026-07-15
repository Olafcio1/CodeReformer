from typing import Generic, TypeVar, Callable, Any

S = TypeVar('S')

class StyleProxy(Generic[S]):
	__obj: S
	__callback: Callable[[], S]

	def __init__(self, obj: S, callback: Callable[[], S]):
		self.__obj = obj
		self.__callback = callback

	def __call__(self, *args: Any, **kwargs: Any):
		return object.__getattribute__(self, '_StyleProxy__obj')(*args, **kwargs)

	def __getattr__(self, name: str):
		return getattr(object.__getattribute__(self, '_StyleProxy__callback')(name), name)

	def __setattr__(self, name: str, value: Any):
		if name.startswith('_StyleProxy__'):
			object.__setattr__(self, name, value)
		else:
			setattr(self.__obj, name, value)

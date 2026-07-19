from typing import TypeVar, TypeVarTuple, Callable, Any

Arg1 = TypeVarTuple("Arg1")
Args = TypeVarTuple("Args")
Ret = TypeVar("Ret")

def invoker(callable: Callable[[*Arg1, *Args], Ret], *args: *Args) -> Callable[[*Arg1], Ret]:
	def gen(*arg: Any, **kwarg: Any) -> Ret:
		nonlocal args
		return callable(*arg, *args, **kwarg)

	return gen

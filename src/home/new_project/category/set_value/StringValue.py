from typing import Callable, final, overload

Validator = Callable[[str], bool]

@final
class StringValue:
    """A string value. Should be shown as a text input in the UI."""

    value: str
    validator: Validator|None

    @overload
    def __init__(self, /):
        ...

    @overload
    def __init__(self, defaultValue: str, /):
        ...

    @overload
    def __init__(self, validator: Validator, /):
        ...

    @overload
    def __init__(self, defaultValue: str, validator: Validator, /):
        ...

    def __init__(self, *args):
        if len(args) == 0:
            return
        elif len(args) == 1:
            if isinstance(args[0], str):
                self.value = args[0]
                return
            elif isinstance(args[0], Callable):
                self.validator = args[0]
                return
        elif len(args) == 2:
            self.value, self.validator = args
            return

        raise Exception("No matching overload")

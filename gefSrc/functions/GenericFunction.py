from gefSrc.util.helper import is_alive
from typing import (List, Any)
import gdb


class GenericFunction(gdb.Function):
    """This is an abstract class for invoking convenience functions, should not be instantiated."""

    _function_ : str
    _syntax_: str = ""
    _example_ : str = ""

    def __init__(self) -> None:
        super().__init__(self._function_)

    def invoke(self, *args: Any) -> int:
        if not is_alive():
            raise gdb.GdbError("No debugging session active")
        return self.do_invoke(args)

    def arg_to_long(self, args: List, index: int, default: int = 0) -> int:
        try:
            addr = args[index]
            return int(addr) if addr.address is None else int(addr.address)
        except IndexError:
            return default

    def do_invoke(self, args: Any) -> int:
        raise NotImplementedError

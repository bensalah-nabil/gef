from gefSrc.util.helper import is_alive
from gefSrc.util.display_helper import warn
from gefSrc.util.helper import is_remote_debug
from typing import (Callable, Any)
import functools


def only_if_gdb_running(f: Callable) -> Callable:
    """Decorator wrapper to check if GDB is running."""

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if is_alive():
            return f(*args, **kwargs)
        else:
            warn("No debugging session active")

    return wrapper


def only_if_gdb_target_local(f: Callable) -> Callable:
    """Decorator wrapper to check if GDB is running locally (target not remote)."""

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not is_remote_debug():
            return f(*args, **kwargs)
        else:
            warn("This command cannot work for remote sessions.")

    return wrapper

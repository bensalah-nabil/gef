from gefSrc.util.helper import is_alive
from gefSrc.util.display_helper import warn
from gefSrc.util.helper import is_remote_debug
from gefSrc.globals import RunTimeGlobals
from typing import (Callable, Any)
import functools
import pathlib
import inspect


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


def deprecated(solution: str = "") -> Callable:
    """Decorator to add a warning when a command is obsolete and will be removed."""
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            caller = inspect.stack()[1]
            caller_file = pathlib.Path(caller.filename)
            caller_loc = caller.lineno
            msg = f"{caller_file.name}:L{caller_loc} '{f.__name__}' is deprecated and will be removed in a feature release. "
            if not gef:
                print(msg)
            elif RunTimeGlobals.gef.config["RunTimeGlobals.gef.show_deprecation_warnings"] is True:
                if solution:
                    msg += solution
                warn(msg)
            return f(*args, **kwargs)

        if not wrapper.__doc__:
            wrapper.__doc__ = ""
        wrapper.__doc__ += f"\r\n`{f.__name__}` is **DEPRECATED** and will be removed in the future.\r\n{solution}"
        return wrapper
    return decorator


def experimental_feature(f: Callable) -> Callable:
    """Decorator to add a warning when a feature is experimental."""

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        warn("This feature is under development, expect bugs and unstability...")
        return f(*args, **kwargs)

    return wrapper
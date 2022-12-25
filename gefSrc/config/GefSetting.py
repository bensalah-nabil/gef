from typing import (List, Callable, Any, Tuple, Optional, Dict)


class GefSetting:
    """Basic class for storing gef settings as objects"""
    READ_ACCESS = 0
    WRITE_ACCESS = 1

    def __init__(self, value: Any, cls: Optional[type] = None, description: Optional[str] = None, hooks: Optional[Dict[str, Callable]] = None)  -> None:
        self.value = value
        self.type = cls or type(value)
        self.description = description or ""
        self.hooks: Tuple[List[Callable], List[Callable]] = ([], [])
        if hooks:
            for access, func in hooks.items():
                if access == "on_read":
                    idx = GefSetting.READ_ACCESS
                elif access == "on_write":
                    idx = GefSetting.WRITE_ACCESS
                else:
                    raise ValueError
                if not callable(func):
                    raise ValueError(f"hook is not callable")
                self.hooks[idx].append(func)
        return

    def __str__(self) -> str:
        return f"Setting(type={self.type.__name__}, value='{self.value}', desc='{self.description[:10]}...', "\
            f"read_hooks={len(self.hooks[GefSetting.READ_ACCESS])}, write_hooks={len(self.hooks[GefSetting.READ_ACCESS])})"


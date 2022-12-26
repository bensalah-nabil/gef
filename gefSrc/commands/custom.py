from gefSrc.util.display_helper import clear_screen, gef_print
from gefSrc.commands.GenericCommand import GenericCommand
from gefSrc.util.register_feature import register
from typing import List


@register
class ClearScreenCommand(GenericCommand):
    """Clear the screen"""

    _cmdline_ = "clear"
    _syntax_ = f"{_cmdline_}"
    _example_ = f"{_cmdline_}"

    def __init__(self) -> None:
        super().__init__()
        return
    
    def do_invoke(self, _: List[str]) -> None:
        clear_screen()
        return


@register
class LibcInfoCommand(GenericCommand):
    """Command to get libc version & base."""

    _cmdline_ = "libc"
    _syntax_ = f"{_cmdline_}"
    _example_ = f"{_cmdline_}"

    def __init__(self) -> None:
        super().__init__()
        return
    
    def do_invoke(self, _: List[str]) -> None:
        
        gef_print(f"Libc Base: {hex(RunTimeGlobals.gef.libc.base_address)}")
        gef_print(f"Libc Version: {'.'.join(map(str,RunTimeGlobals.gef.libc.version))}")
        return

from gefSrc.globals import RunTimeGlobals
from gefSrc.util.Color import Color
from gefSrc.config import Config
from gefSrc.util.helper import is_debug
from gefSrc.globals import RunTimeGlobals
import re
from typing import Any
import gdb



def highlight_text(text: str) -> str:
    """
    Highlight text using `gef.ui.highlight_table` { match -> color } settings.

    If RegEx is enabled it will create a match group around all items in the
    `gef.ui.highlight_table` and wrap the specified color in the `gef.ui.highlight_table`
    around those matches.

    If RegEx is disabled, split by ANSI codes and 'colorify' each match found
    within the specified string.
    """
    if not RunTimeGlobals.gef.ui.highlight_table:
        return text

    if RunTimeGlobals.gef.config["highlight.regex"]:
        for match, color in RunTimeGlobals.gef.ui.highlight_table.items():
            text = re.sub("(" + match + ")", Color.colorify("\\1", color), text)
        return text

    ansiSplit = re.split(Config.ANSI_SPLIT_RE, text)

    for match, color in RunTimeGlobals.gef.ui.highlight_table.items():
        for index, val in enumerate(ansiSplit):
            found = val.find(match)
            if found > -1:
                ansiSplit[index] = val.replace(match, Color.colorify(match, color))
                break
        text = "".join(ansiSplit)
        ansiSplit = re.split(Config.ANSI_SPLIT_RE, text)

    return "".join(ansiSplit)


def buffer_output() -> bool:
    """Check if output should be buffered until command completion."""
    return RunTimeGlobals.gef.config["RunTimeGlobals.gef.buffer"] is True


def gef_print(*args: str, end="\n", sep=" ", **kwargs: Any) -> None:
    """Wrapper around print(), using string buffering feature."""
    parts = [highlight_text(a) for a in args]
    if buffer_output() and RunTimeGlobals.gef.ui.stream_buffer and not is_debug():
        RunTimeGlobals.gef.ui.stream_buffer.write(sep.join(parts) + end)
        return

    print(*parts, sep=sep, end=end, **kwargs)
    return


def dbg(msg: str) -> None:
    if RunTimeGlobals.gef.config["RunTimeGlobals.gef.debug"] is True:
        gef_print(f"{Color.colorify('[=]', 'bold cyan')} {msg}")
    return


def err(msg: str) -> None:
    gef_print(f"{Color.colorify('[!]', 'bold red')} {msg}")
    return


def warn(msg: str) -> None:
    gef_print(f"{Color.colorify('[*]', 'bold yellow')} {msg}")
    return


def ok(msg: str) -> None:
    gef_print(f"{Color.colorify('[+]', 'bold green')} {msg}")
    return


def info(msg: str) -> None:
    gef_print(f"{Color.colorify('[+]', 'bold blue')} {msg}")
    return


def clear_screen(tty: str = "") -> None:
    """Clear the screen."""
    if not tty:
        gdb.execute("shell clear -x")
        return

    # Since the tty can be closed at any time, a PermissionError exception can
    # occur when `clear_screen` is called. We handle this scenario properly
    try:
        with open(tty, "wt") as f:
            f.write("\x1b[H\x1b[J")
    except PermissionError:
        RunTimeGlobals.gef.ui.redirect_fd = None
        RunTimeGlobals.gef.config["context.redirect"] = ""
    return

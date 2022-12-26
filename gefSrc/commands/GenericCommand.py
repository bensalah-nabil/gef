from gefSrc.globals import RunTimeGlobals
from gefSrc.util.Color import Color
from gefSrc.config import GefSetting
from gefSrc.util.helper import is_debug
from gefSrc.util.display_helper import err
from typing import (Union, List, Callable, Any, Generator, Tuple)
from io import StringIO
import functools
import gdb, sys


class GenericCommand(gdb.Command):
    """This is an abstract class for invoking commands, should not be instantiated."""

    _cmdline_: str
    _syntax_: str
    _example_: Union[str, List[str]] = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        attributes = ("_cmdline_", "_syntax_", )
        if not all(map(lambda x: hasattr(cls, x), attributes)):
            raise NotImplementedError

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.pre_load()
        syntax = Color.yellowify("\nSyntax: ") + self._syntax_
        example = Color.yellowify("\nExamples: \n\t")
        if isinstance(self._example_, list):
            example += "\n\t".join(self._example_)
        elif isinstance(self._example_, str):
            example += self._example_
        self.__doc__ = self.__doc__.replace(" "*4, "") + syntax + example
        self.repeat = False
        self.repeat_count = 0
        self.__last_command = None
        command_type = kwargs.setdefault("command", gdb.COMMAND_OBSCURE)
        complete_type = kwargs.setdefault("complete", gdb.COMPLETE_NONE)
        prefix = kwargs.setdefault("prefix", False)
        super().__init__(self._cmdline_, command_type, complete_type, prefix)
        self.post_load()
        return

    def invoke(self, args: str, from_tty: bool) -> None:
        try:
            argv = gdb.string_to_argv(args)
            self.__set_repeat_count(argv, from_tty)
            bufferize(self.do_invoke)(argv)
        except Exception as e:
            # Note: since we are intercepting cleaning exceptions here, commands preferably should avoid
            # catching generic Exception, but rather specific ones. This is allows a much cleaner use.
            if is_debug():
                show_last_exception()
            else:
                err(f"Command '{self._cmdline_}' failed to execute properly, reason: {e}")
        return

    def usage(self) -> None:
        err(f"Syntax\n{self._syntax_}")
        return

    def do_invoke(self, argv: List[str]) -> None:
        raise NotImplementedError

    def pre_load(self) -> None:
        return

    def post_load(self) -> None:
        return

    def __get_setting_name(self, name: str) -> str:
        clsname = self.__class__._cmdline_.replace(" ", "-")
        return f"{clsname}.{name}"

    def __iter__(self) -> Generator[str, None, None]:
        for key in RunTimeGlobals.gef.config.keys():
            if key.startswith(self._cmdline_):
                yield key.replace(f"{self._cmdline_}.", "", 1)

    @property
    def settings(self) -> List[str]:
        """Return the list of settings for this command."""
        return list(iter(self))

    def __getitem__(self, name: str) -> Any:
        key = self.__get_setting_name(name)
        return RunTimeGlobals.gef.config[key]

    def __contains__(self, name: str) -> bool:
        return self.__get_setting_name(name) in RunTimeGlobals.gef.config

    def __setitem__(self, name: str, value: Union[Any, Tuple[Any, str]]) -> None:
        # make sure settings are always associated to the root command (which derives from GenericCommand)
        if "GenericCommand" not in [x.__name__ for x in self.__class__.__bases__]:
            return
        key = self.__get_setting_name(name)
        if key in RunTimeGlobals.gef.config:
            setting = RunTimeGlobals.gef.config.raw_entry(key)
            setting.value = value
        else:
            if len(value) == 1:
                RunTimeGlobals.gef.config[key] = GefSetting(value[0])
            elif len(value) == 2:
                RunTimeGlobals.gef.config[key] = GefSetting(value[0], description=value[1])
        return

    def __delitem__(self, name: str) -> None:
        del RunTimeGlobals.gef.config[self.__get_setting_name(name)]
        return

    def __set_repeat_count(self, argv: List[str], from_tty: bool) -> None:
        if not from_tty:
            self.repeat = False
            self.repeat_count = 0
            return

        command = gdb.execute("show commands", to_string=True).strip().split("\n")[-1]
        self.repeat = self.__last_command == command
        self.repeat_count = self.repeat_count + 1 if self.repeat else 0
        self.__last_command = command
        return



def bufferize(f: Callable) -> Callable:
    """Store the content to be printed for a function in memory, and flush it on function exit."""

    @functools.wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        global gef

        if RunTimeGlobals.gef.ui.stream_buffer:
            return f(*args, **kwargs)

        RunTimeGlobals.gef.ui.stream_buffer = StringIO()
        try:
            rv = f(*args, **kwargs)
        finally:
            redirect = RunTimeGlobals.gef.config["context.redirect"]
            if redirect.startswith("/dev/pts/"):
                if not RunTimeGlobals.gef.ui.redirect_fd:
                    # if the FD has never been open, open it
                    fd = open(redirect, "wt")
                    RunTimeGlobals.gef.ui.redirect_fd = fd
                elif redirect != RunTimeGlobals.gef.ui.redirect_fd.name:
                    # if the user has changed the redirect setting during runtime, update the state
                    RunTimeGlobals.gef.ui.redirect_fd.close()
                    fd = open(redirect, "wt")
                    RunTimeGlobals.gef.ui.redirect_fd = fd
                else:
                    # otherwise, keep using it
                    fd = RunTimeGlobals.gef.ui.redirect_fd
            else:
                fd = sys.stdout
                RunTimeGlobals.gef.ui.redirect_fd = None
            
            if RunTimeGlobals.gef.ui.redirect_fd and fd.closed:
                # if the tty was closed, revert back to stdout
                fd = sys.stdout
                RunTimeGlobals.gef.ui.redirect_fd = None
                RunTimeGlobals.gef.config["context.redirect"] = ""

            fd.write(RunTimeGlobals.gef.ui.stream_buffer.getvalue())
            fd.flush()
            RunTimeGlobals.gef.ui.stream_buffer = None
        return rv

    return wrapper

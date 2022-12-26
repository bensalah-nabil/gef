from gefSrc.globals import GlobalRegistered
from typing import (Union, Type)


def register(cls: Union[Type["GenericCommand"], Type["GenericFunction"]]) -> Union[Type["GenericCommand"], Type["GenericFunction"]]:
    from gefSrc.commands.GenericCommand import GenericCommand
    from gefSrc.functions.GenericFunction import GenericFunction
    
    if issubclass(cls, GenericCommand):
        assert( hasattr(cls, "_cmdline_"))
        assert( hasattr(cls, "do_invoke"))
        assert( all(map(lambda x: x._cmdline_ != cls._cmdline_, GlobalRegistered.commands)))
        GlobalRegistered.commands.add(cls)
        return cls

    if issubclass(cls, GenericFunction):
        assert( hasattr(cls, "_function_"))
        assert( hasattr(cls, "invoke"))
        assert( all(map(lambda x: x._function_ != cls._function_, GlobalRegistered.functions)))
        GlobalRegistered.functions.add(cls)
        return cls

    raise TypeError(f"`{cls.__class__}` is an illegal class for `register`")

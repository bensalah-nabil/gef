from typing import (Set, Type, Dict, Union)


class GlobalRegistered:
    commands : Set[Type["GenericCommand"]]                                        = set()
    functions : Set[Type["GenericFunction"]]                                      = set()
    architectures : Dict[Union["Elf.Abi", str], Type["Architecture"]]              = {}
    file_formats : Set[ Type["FileFormat"] ]                                       = set()

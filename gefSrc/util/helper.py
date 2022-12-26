from typing import (Optional)
import struct
import gdb
import traceback
from gefSrc.globals import RunTimeGlobals


def p8(x: int, s: bool = False, e: Optional["Endianness"] = None) -> bytes:
    """Pack one byte respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.pack(f"{endian}B", x) if not s else struct.pack(f"{endian:s}b", x)


def p16(x: int, s: bool = False, e: Optional["Endianness"] = None) -> bytes:
    """Pack one word respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.pack(f"{endian}H", x) if not s else struct.pack(f"{endian:s}h", x)


def p32(x: int, s: bool = False, e: Optional["Endianness"] = None) -> bytes:
    """Pack one dword respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.pack(f"{endian}I", x) if not s else struct.pack(f"{endian:s}i", x)


def p64(x: int, s: bool = False, e: Optional["Endianness"] = None) -> bytes:
    """Pack one qword respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.pack(f"{endian}Q", x) if not s else struct.pack(f"{endian:s}q", x)


def u8(x: bytes, s: bool = False, e: Optional["Endianness"] = None) -> int:
    """Unpack one byte respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.unpack(f"{endian}B", x)[0] if not s else struct.unpack(f"{endian:s}b", x)[0]


def u16(x: bytes, s: bool = False, e: Optional["Endianness"] = None) -> int:
    """Unpack one word respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.unpack(f"{endian}H", x)[0] if not s else struct.unpack(f"{endian:s}h", x)[0]


def u32(x: bytes, s: bool = False, e: Optional["Endianness"] = None) -> int:
    """Unpack one dword respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.unpack(f"{endian}I", x)[0] if not s else struct.unpack(f"{endian:s}i", x)[0]


def u64(x: bytes, s: bool = False, e: Optional["Endianness"] = None) -> int:
    """Unpack one qword respecting the current architecture endianness."""
    global gef
    endian = e or RunTimeGlobals.gef.arch.endianness
    return struct.unpack(f"{endian}Q", x)[0] if not s else struct.unpack(f"{endian:s}q", x)[0]

def is_ascii_string(address: int) -> bool:
    """Helper function to determine if the buffer pointed by `address` is an ASCII string (in GDB)"""
    global gef
    try:
        return RunTimeGlobals.gef.memory.read_ascii_string(address) is not None
    except Exception:
        return False


def is_alive() -> bool:
    """Check if GDB is running."""
    try:
        return gdb.selected_inferior().pid > 0
    except Exception:
        return False


def calling_function() -> Optional[str]:
    """Return the name of the calling function"""
    try:
        stack_info = traceback.extract_stack()[-3]
        return stack_info.name
    except:
        return None


def is_debug() -> bool:
    """Check if debug mode is enabled."""
    return RunTimeGlobals.gef.config["RunTimeGlobals.gef.debug"] is True


def is_remote_debug() -> bool:
    """"Return True is the current debugging session is running through GDB remote session."""
    return RunTimeGlobals.gef.session.remote_initializing or RunTimeGlobals.gef.session.remote is not None

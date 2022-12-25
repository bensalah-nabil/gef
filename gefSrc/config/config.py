import re, os, sys, pathlib
import gdb
import tempfile

class Config:
    GEF_DEFAULT_BRANCH                     = "main"
    GEF_EXTRAS_DEFAULT_BRANCH              = "main"

    GDB_MIN_VERSION                        = (8, 0)
    GDB_VERSION                            = tuple(map(int, re.search(r"(\d+)[^\d]+(\d+)", gdb.VERSION).groups()))
    PYTHON_MIN_VERSION                     = (3, 6)
    PYTHON_VERSION                         = sys.version_info[0:2]

    DEFAULT_PAGE_ALIGN_SHIFT               = 12
    DEFAULT_PAGE_SIZE                      = 1 << DEFAULT_PAGE_ALIGN_SHIFT

    GEF_RC                                 = (pathlib.Path(os.getenv("GEF_RC", "")).absolute()
                                            if os.getenv("GEF_RC")
                                            else pathlib.Path().home() / ".gef.rc")
    GEF_TEMP_DIR                           = os.path.join(tempfile.gettempdir(), "gef")
    GEF_MAX_STRING_LENGTH                  = 50

    LIBC_HEAP_MAIN_ARENA_DEFAULT_NAME      = "main_arena"
    ANSI_SPLIT_RE                          = r"(\033\[[\d;]*m)"

    PATTERN_LIBC_VERSION                   = re.compile(rb"glibc (\d+)\.(\d+)")

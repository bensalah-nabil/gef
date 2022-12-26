from gefSrc.config import Config
from urllib.request import urlopen
from typing import (Optional, List)


def http_get(url: str) -> Optional[bytes]:
    """Basic HTTP wrapper for GET request. Return the body of the page if HTTP code is OK,
    otherwise return None."""
    try:
        http = urlopen(url)
        return http.read() if http.getcode() == 200 else None
    except Exception:
        return None


def update_gef(argv: List[str]) -> int:
    """Try to update `gef` to the latest version pushed on GitHub main branch.
    Return 0 on success, 1 on failure. """
    ver = "dev" if "--dev" in argv else Config.GEF_DEFAULT_BRANCH
    latest_gef_data = http_get(f"https://raw.githubusercontent.com/hugsy/gef/{ver}/scripts/gef.sh")
    if not latest_gef_data:
        print("[-] Failed to get remote gef")
        return 1
    with tempfile.NamedTemporaryFile(suffix=".sh") as fd:
        fd.write(latest_gef_data)
        fd.flush()
        fpath = pathlib.Path(fd.name)
        return subprocess.run(["bash", fpath, ver], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL).returncode

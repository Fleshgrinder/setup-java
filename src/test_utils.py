from contextlib import contextmanager
from io import StringIO
from os import getcwd, chdir
from pathlib import Path
from shutil import rmtree

RESET = "\033[0m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


def read_text(io: StringIO) -> str:
    io.seek(0)
    return io.read()


@contextmanager
def cwd(path: Path):
    cur = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(cur)
        rmtree(path)

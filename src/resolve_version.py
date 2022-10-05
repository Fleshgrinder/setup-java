#!/usr/bin/env python3
import traceback
from pathlib import Path
from typing import Any, IO, Dict


def _resolve_version(env: Dict[str, str], io: IO[str], v: str, src: Any) -> int:
    with Path(env["GITHUB_ENV"]).open("a") as fh:
        fh.write(f"JAVA_VERSION={v}\n")
    io.write(f"Resolved version \033[32m{v}\033[0m from \033[36m{src}\033[0m and exported it as \033[33mJAVA_VERSION\033[0m to the environment.\n")
    return 0


def resolve_version(env: Dict[str, str], io: IO[str]) -> int:
    if not env.get("GITHUB_ENV", "").strip():
        io.write("::error::Missing required environment variable GITHUB_ENV, make sure it exists.\n")
        return 1

    input_version = env.get("INPUT_VERSION", "").strip()
    if input_version:
        return _resolve_version(env, io, input_version, "input")

    version_file = Path(env.get("INPUT_VERSION_FILENAME", "").strip() or env.get("JAVA_DEFAULT_VERSION_FILENAME", "").strip() or ".java-version")
    if version_file.exists():
        try:
            with version_file.open("r") as fh:
                version = fh.readline().strip()
                if version:
                    return _resolve_version(env, io, version, version_file)
                else:
                    io.write(f"::error file={version_file}::Invalid version, '{version_file}' must not be blank.\n")
                    return 2
        except IOError:
            if version_file.is_file():
                traceback.print_exc()
                io.write(f"::error file={version_file}::Could not read file '{version_file}', see build log for more information.\n")
                return 3
            else:
                io.write(f"::error file={version_file}::Invalid file type, '{version_file}' must be a regular file.\n")
                return 4
    else:
        default_version = env.get("JAVA_DEFAULT_VERSION", "").strip()
        if default_version:
            return _resolve_version(env, io, default_version, "JAVA_DEFAULT_VERSION")
        else:
            io.write(f"::error file={version_file}::Missing required file '{version_file}', make sure it exists.\n")
            return 5


if __name__ == "__main__":  # pragma: no cover
    import os
    import sys

    resolve_version(dict(os.environ), sys.stdout)

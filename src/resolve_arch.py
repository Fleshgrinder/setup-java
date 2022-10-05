#!/usr/bin/env python3
from typing import IO, Dict


def resolve_arch(env: Dict[str, str], io: IO[str]) -> int:
    runner_arch = env.get("RUNNER_ARCH", "").strip()
    if not runner_arch:
        io.write("::error::Missing required environment variable RUNNER_ARCH, make sure it exists.\n")
        return 1

    arch = runner_arch.lower()
    if arch == "x64" or arch == "x86":
        pass
    elif arch == "arm":
        arch = "armv7"
    elif arch == "arm64":
        arch = "aarch64"
    else:
        io.write(f"""\
::error::Unknown architecture '{runner_arch}', please open an issue at https://github.com/fleshgrinder/setup-java/issues \
so that support for it can be added to the setup action. Continuing with '{arch}', which might, or might not work.
""")

    io.write(f"::set-output name=value::{arch}\n")
    io.write(f"Resolved architecture \033[32m{arch}\033[0m from \033[33m{runner_arch}\033[0m.\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    import os
    import sys

    resolve_arch(dict(os.environ), sys.stdout)

from io import StringIO
from typing import Dict, Optional

import pytest

from resolve_arch import resolve_arch
from test_utils import read_text, RESET, GREEN, YELLOW


def env(runner_arch: Optional[str] = None) -> Dict[str, str]:
    return {} if runner_arch is None else {"RUNNER_ARCH": runner_arch}


@pytest.mark.parametrize("runner_arch", [None, "", " \t "])
def test_fails_if_runner_arch_is_invalid(runner_arch: Optional[str]):
    io = StringIO()
    ec = resolve_arch(env(runner_arch), io)
    assert read_text(io) == "::error::Missing required environment variable RUNNER_ARCH, make sure it exists.\n"
    assert ec == 1


@pytest.mark.parametrize("runner_arch,resolved_arch", [
    ("X86", "x86"),
    ("X64", "x64"),
    ("ARM", "armv7"),
    ("ARM64", "aarch64"),
])
def test_arch_mapping(runner_arch: str, resolved_arch: str):
    io = StringIO()
    ec = resolve_arch(env(runner_arch), io)
    assert read_text(io) == f"""\
::set-output name=value::{resolved_arch}
Resolved architecture {GREEN}{resolved_arch}{RESET} from {YELLOW}{runner_arch}{RESET}.
"""
    assert ec == 0


def test_unknown_arch():
    runner_arch = "RISCV"
    resolved_arch = "riscv"
    io = StringIO()
    ec = resolve_arch(env(runner_arch), io)
    assert read_text(io) == f"""\
::error::Unknown architecture '{runner_arch}', please open an issue at https://github.com/fleshgrinder/setup-java/issues \
so that support for it can be added to the setup action. Continuing with '{resolved_arch}', which might, or might not work.
::set-output name=value::{resolved_arch}
Resolved architecture {GREEN}{resolved_arch}{RESET} from {YELLOW}{runner_arch}{RESET}.
"""
    assert ec == 0

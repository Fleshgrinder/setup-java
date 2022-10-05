import os
from io import StringIO
from pathlib import Path
from typing import Dict, Union, Optional
from uuid import uuid4

import pytest

from resolve_version import resolve_version
from test_utils import read_text, cwd, GREEN, RESET, CYAN, YELLOW


def env(
    github_env: Optional[Union[Path, str]] = None,
    version_input: Optional[Union[int, str]] = None,
    version_file: Optional[Union[Path, str]] = None,
    version_default: Optional[Union[int, str]] = None,
) -> Dict[str, str]:
    _env = {}
    if github_env is not None:
        _env["GITHUB_ENV"] = str(github_env)
    if version_input is not None:
        _env["INPUT_VERSION"] = str(version_input)
    if version_file is not None:
        _env["INPUT_VERSION_FILENAME"] = str(version_file)
    if version_default is not None:
        _env["JAVA_DEFAULT_VERSION"] = str(version_default)
    return _env


@pytest.mark.parametrize("github_env", [None, "", " \t "])
def test_fails_if_runner_arch_is_invalid(github_env: Optional[str]):
    io = StringIO()
    ec = resolve_version(env(github_env=github_env), io)
    assert read_text(io) == "::error::Missing required environment variable GITHUB_ENV, make sure it exists.\n"
    assert ec == 1


def test_uses_input_version_if_present(tmp_path: Path):
    with cwd(tmp_path):
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_input="42"), io)
        assert github_env.read_text() == "JAVA_VERSION=42\n"
        assert read_text(io) == f"""\
Resolved version {GREEN}42{RESET} from {CYAN}input{RESET} and exported it as {YELLOW}JAVA_VERSION{RESET} to the environment.
"""
        assert ec == 0


def test_fails_if_java_version_file_does_not_exist_and_no_default_version_is_defined(tmp_path: Path):
    with cwd(tmp_path):
        file = f"non-existing-file-{uuid4()}"
        github_env = (tmp_path / "env")
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_file=file), io)
        assert github_env.exists() is False
        assert read_text(io) == f"::error file={file}::Missing required file '{file}', make sure it exists.\n"
        assert ec == 5


@pytest.mark.parametrize("version_file", [".java-version", ".jvm-version"])
def test_uses_java_version_from_file_if_file_exists(version_file: Optional[str], tmp_path: Path):
    with cwd(tmp_path):
        (tmp_path / version_file).write_text("  42\t  ")
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(
            env(
                github_env=github_env,
                version_default="not me, no!",
                version_file=None if version_file == ".java-version" else version_file,
            ),
            io,
        )
        assert github_env.read_text() == "JAVA_VERSION=42\n"
        assert read_text(io) == f"""\
Resolved version {GREEN}42{RESET} from {CYAN}{version_file}{RESET} and exported it as {YELLOW}JAVA_VERSION{RESET} to the environment.
"""
        assert ec == 0


@pytest.mark.parametrize("java_version", ["", " \t "])
def test_fails_if_java_version_file_is_blank(java_version: str, tmp_path: Path):
    with cwd(tmp_path):
        (tmp_path / ".java-version").write_text(java_version)
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_default="not me, not!"), io)
        assert github_env.exists() is False
        assert read_text(io) == f"::error file=.java-version::Invalid version, '.java-version' must not be blank.\n"
        assert ec == 2


@pytest.mark.skipif(os.sep == "\\", reason="Windows permissions work differently.")
def test_fails_if_java_version_file_cannot_be_read(tmp_path: Path):
    with cwd(tmp_path):
        (tmp_path / ".java-version").touch(mode=0o222)
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_default="not me, not!"), io)
        assert github_env.exists() is False
        assert read_text(io) == f"::error file=.java-version::Could not read file '.java-version', see build log for more information.\n"
        assert ec == 3


def test_fails_if_java_version_file_is_not_a_file(tmp_path: Path):
    with cwd(tmp_path):
        (tmp_path / ".java-version").mkdir()
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_default="not me, not!"), io)
        assert github_env.exists() is False
        assert read_text(io) == f"::error file=.java-version::Invalid file type, '.java-version' must be a regular file.\n"
        assert ec == 4


def test_uses_default_version_if_no_file_exists(tmp_path: Path):
    with cwd(tmp_path):
        github_env = tmp_path / "env"
        io = StringIO()
        ec = resolve_version(env(github_env=github_env, version_default="42"), io)
        assert github_env.read_text() == "JAVA_VERSION=42\n"
        assert read_text(io) == f"""\
Resolved version {GREEN}42{RESET} from {CYAN}JAVA_DEFAULT_VERSION{RESET} and exported it as {YELLOW}JAVA_VERSION{RESET} to the environment.
"""
        assert ec == 0

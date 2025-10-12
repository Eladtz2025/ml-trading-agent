"""Utilities for executing subprocess commands with friendly errors."""

from __future__ import annotations

import subprocess
from typing import Sequence


class SubprocessError(RuntimeError):
    """Raised when a subprocess exits with a non-zero status code."""

    def __init__(self, command: Sequence[str], exit_code: int, stderr: str | None = None) -> None:
        message = "Command failed with exit code {code}: {cmd}".format(
            code=exit_code,
            cmd=" ".join(command),
        )
        if stderr:
            message = f"{message}\n{stderr.strip()}"
        super().__init__(message)
        self.command = tuple(command)
        self.exit_code = exit_code
        self.stderr = stderr


def run(command: Sequence[str]) -> None:
    """Run a command, raising :class:`SubprocessError` if it fails."""

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:  # pragma: no cover - thin wrapper
        stderr = None
        if error.stderr:
            stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else str(error.stderr)
        raise SubprocessError(command, error.returncode, stderr) from error

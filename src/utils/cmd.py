"""
Command execution helpers for SAFEX scanners.

Centralizes subprocess handling so every scanner gets consistent behaviour:
- deterministic timeout handling
- safe handling of missing binaries (returns rc 127, no exception)
- UTF-8 text output with surrogateescape so binary garbage never crashes a scan
- structured CommandResult for easy assertions in tests
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import List, Optional, Sequence, Union

from .logger import get_logger

logger = get_logger(__name__)

# Return code used when a binary is not present on the system. Mirrors the
# conventional shell value so callers can treat it identically to /bin/sh.
CMD_NOT_FOUND_RC = 127

# Default per-command timeout. Individual callers may override.
DEFAULT_TIMEOUT = 15


@dataclass
class CommandResult:
    """Structured result of a shell command."""

    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run_cmd(
    command: Union[str, Sequence[str]],
    *,
    timeout: int = DEFAULT_TIMEOUT,
    input_text: Optional[str] = None,
    shell: Optional[bool] = None,
) -> CommandResult:
    """Run a command safely and return a :class:`CommandResult`.

    Args:
        command: Either a string (run via shell) or a list of arguments
            (run without shell). When ``shell`` is explicitly provided it takes
            precedence over the automatic detection.
        timeout: Maximum seconds to wait before killing the process.
        input_text: Optional stdin payload.
        shell: Force shell/no-shell. If ``None`` it is ``True`` for ``str``
            commands and ``False`` for sequences.

    Returns:
        CommandResult. Never raises for missing binaries or timeouts — those
        are logged and returned as structured failures so a scan keeps going.
    """
    if shell is None:
        shell = isinstance(command, str)

    try:
        proc = subprocess.run(
            command,
            shell=shell,
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return CommandResult(
            returncode=proc.returncode,
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
        )
    except FileNotFoundError:
        # Binary missing — common during scans (e.g. no nmap installed).
        return CommandResult(CMD_NOT_FOUND_RC, "", "command not found")
    except subprocess.TimeoutExpired:
        logger.warning("Command timed out after %ss: %s", timeout, command)
        return CommandResult(124, "", f"timeout after {timeout}s")
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Command failed (%s): %s", exc, command)
        return CommandResult(1, "", str(exc))


def read_file_lines(path: str, max_bytes: int = 5_000_000) -> List[str]:
    """Read a (potentially large) text file as a list of lines.

    Reads in UTF-8 with replacement so malformed bytes never crash a scan.
    A ``max_bytes`` guard prevents runaway memory on huge log files.
    Missing files return an empty list.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            data = fh.read(max_bytes)
        return data.splitlines()
    except FileNotFoundError:
        return []
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("Cannot read %s: %s", path, exc)
        return []

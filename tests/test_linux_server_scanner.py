"""
Tests for the Linux server security scanner.

All filesystem and subprocess access is mocked so the suite is deterministic
and runs on Windows CI as well as Linux. The tests focus on the logic that
previously produced false negatives (the "thermometer" behaviour):
brute-force severity, dangerous-port detection, and the zombie process fix.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.scanners import linux_server_scanner as lss
from src.scanners.linux_server_scanner import LinuxServerScanner
from src.utils.cmd import CommandResult


# --------------------------------------------------------------------------- #
# Pure helpers
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "count,expected",
    [
        (0, "INFO"),
        (9, "INFO"),
        (10, "LOW"),
        (49, "LOW"),
        (50, "MEDIUM"),
        (199, "MEDIUM"),
        (200, "HIGH"),
        (999, "HIGH"),
        (1000, "CRITICAL"),
        (3950, "CRITICAL"),  # the real attack size from the bug report
    ],
)
def test_severity_for_failed_logins(count, expected):
    assert lss.severity_for_failed_logins(count) == expected


def test_parse_sshd_config_reads_active_directives(tmp_path):
    cfg = tmp_path / "sshd_config"
    cfg.write_text(
        "#PermitRootLogin yes\n"
        "PermitRootLogin no\n"
        "PasswordAuthentication no\n"
        "UsePAM yes\n",
        encoding="utf-8",
    )
    parsed = LinuxServerScanner._parse_sshd_config(str(cfg))
    assert parsed["PermitRootLogin"] == "no"
    assert parsed["PasswordAuthentication"] == "no"
    assert parsed["UsePAM"] == "yes"


def test_parse_sshd_config_defaults_when_missing(tmp_path):
    parsed = LinuxServerScanner._parse_sshd_config(str(tmp_path / "missing"))
    assert parsed == {}


# --------------------------------------------------------------------------- #
# Port helpers
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "addr,public",
    [
        ("0.0.0.0", True),
        ("*", True),
        ("::", True),
        ("", True),
        ("127.0.0.1", False),
        ("::1", False),
        ("192.168.1.5", True),
    ],
)
def test_is_public_bind(addr, public):
    assert LinuxServerScanner._is_public_bind(addr) is public


@pytest.mark.parametrize(
    "local,expected_port,expected_addr",
    [
        ("0.0.0.0:5432", 5432, "0.0.0.0"),
        ("127.0.0.1:631", 631, "127.0.0.1"),
        ("[::]:6379", 6379, "[::]"),
        ("*:22", 22, "*"),
    ],
)
def test_parse_local_address(local, expected_port, expected_addr):
    assert LinuxServerScanner._parse_port(local) == expected_port
    assert LinuxServerScanner._parse_addr(local) == expected_addr


def test_extract_jails():
    out = "Status\n|- Number of jail: 2\n`- Jail list: sshd, recidive\n"
    assert LinuxServerScanner._extract_jails(out) == ["sshd", "recidive"]


def test_extract_jails_empty():
    assert LinuxServerScanner._extract_jails("no jails here") == []


# --------------------------------------------------------------------------- #
# Zombie process fix (the core regression)
# --------------------------------------------------------------------------- #


def test_proc_state_parses_state_char():
    # comm contains parens+spaces on purpose to exercise rfind logic
    stat = "1234 ((a b)) S 1 1234 1234 0 -1 4194304 ...\n"
    assert LinuxServerScanner._proc_state(stat) == "S"


def test_proc_state_handles_zombie():
    stat = "99832 (bash) Z 1 99832 99832 0 -1 ...\n"
    assert LinuxServerScanner._proc_state(stat) == "Z"


def test_proc_state_returns_unknown_on_garbage():
    assert LinuxServerScanner._proc_state("garbage") == "?"


def test_find_live_processes_ignores_zombie_wrapper(tmp_path):
    """The headline bug: a defunct bash wrapper must not count as the service."""
    proc = tmp_path  # stand-in for /proc
    proc_1 = proc / "100"
    proc_2 = proc / "99832"
    proc_1.mkdir()
    proc_2.mkdir()

    # PID 100: real service, alive.
    (proc_1 / "stat").write_text("100 (server_forever) S 1 ...\n", encoding="utf-8")
    (proc_1 / "comm").write_text("server_forever\n", encoding="utf-8")
    # PID 99832: zombie bash wrapper that used to fool ``pgrep -f``.
    (proc_2 / "stat").write_text("99832 (bash) Z 1 ...\n", encoding="utf-8")
    (proc_2 / "comm").write_text("server_forever\n", encoding="utf-8")

    # Materialise BEFORE patching so the lambda never re-enters the mock.
    entries = list(proc.iterdir())
    with mock.patch.object(lss.Path, "iterdir", lambda self: entries), \
         mock.patch.object(lss.Path, "is_dir", lambda self: True):
        pids = LinuxServerScanner._find_live_processes("server_forever")

    assert pids == [100]


def test_find_live_processes_requires_exact_comm(tmp_path):
    """Substring match (the old behaviour) must NOT match."""
    proc = tmp_path
    pid_dir = proc / "500"
    pid_dir.mkdir()
    # comm is "bash" but cmdline contained "server_forever" — must be skipped.
    (pid_dir / "stat").write_text("500 (bash) S 1 ...\n", encoding="utf-8")
    (pid_dir / "comm").write_text("bash\n", encoding="utf-8")

    entries = list(proc.iterdir())
    with mock.patch.object(lss.Path, "iterdir", lambda self: entries), \
         mock.patch.object(lss.Path, "is_dir", lambda self: True):
        assert LinuxServerScanner._find_live_processes("server_forever") == []


# --------------------------------------------------------------------------- #
# Timestamp filtering for brute-force
# --------------------------------------------------------------------------- #


def _make_scanner_with_now(fixed_now: datetime) -> LinuxServerScanner:
    scanner = LinuxServerScanner()
    scanner._now = lambda: fixed_now  # type: ignore[method-assign]
    return scanner


def test_filter_last_24h_keeps_recent_lines():
    now = datetime(2026, 6, 21, 3, 0, 0)
    scanner = _make_scanner_with_now(now)
    recent = "Jun 21 02:30:00 host sshd[1]: Failed password for invalid user root"
    old = "Jun 19 10:00:00 host sshd[1]: Failed password for root"
    kept = scanner._filter_last_24h([recent, old])
    assert recent in kept
    assert old not in kept


def test_filter_last_24h_returns_all_when_no_timestamps():
    now = datetime(2026, 6, 21, 3, 0, 0)
    scanner = _make_scanner_with_now(now)
    lines = ["failed password line with no timestamp", "another line"]
    # When nothing parses we must NOT drop evidence.
    assert scanner._filter_last_24h(lines) == lines


def test_bruteforce_count_uses_full_log(tmp_path):
    """Reproduces the 3950-attempt attack — must surface CRITICAL."""
    now = datetime(2026, 6, 21, 3, 0, 0)
    scanner = _make_scanner_with_now(now)

    auth = tmp_path / "auth.log"
    lines = []
    # 3950 recent failed attempts split across current + rotated log.
    for i in range(3950):
        ts = "Jun 21 02:%02d:%02d" % (i % 60, i % 60)
        lines.append("%s host sshd[%d]: Failed password for root from 1.2.3.4" % (ts, i))
    auth.write_text("\n".join(lines), encoding="utf-8")

    findings = scanner._check_bruteforce(str(auth))
    assert findings[0]["severity"] == "CRITICAL"
    assert findings[0]["failed_logins_24h"] == 3950


def test_bruteforce_reads_rotated_logs(tmp_path):
    now = datetime(2026, 6, 21, 3, 0, 0)
    scanner = _make_scanner_with_now(now)

    base = tmp_path / "auth.log"
    rotated = tmp_path / "auth.log.1"
    base.write_text("Jun 21 02:00:00 host sshd[1]: Failed password for x\n", encoding="utf-8")
    rotated.write_text(
        "Jun 20 22:00:00 host sshd[2]: Failed password for y\n", encoding="utf-8"
    )

    lines = scanner._collect_auth_lines(str(base))
    assert len(lines) == 2


# --------------------------------------------------------------------------- #
# SSH hardening
# --------------------------------------------------------------------------- #


def test_ssh_hardening_flags_insecure_defaults(tmp_path):
    cfg = tmp_path / "sshd_config"
    cfg.write_text(
        "PermitRootLogin yes\nPasswordAuthentication yes\n", encoding="utf-8"
    )
    scanner = LinuxServerScanner()
    with mock.patch.object(
        LinuxServerScanner, "_parse_sshd_config", return_value={
            "PermitRootLogin": "yes", "PasswordAuthentication": "yes",
        }
    ):
        findings = scanner._check_ssh_hardening()
    sev = {f["severity"] for f in findings}
    assert "HIGH" in sev
    assert len(findings) == 2


def test_ssh_hardening_clean():
    scanner = LinuxServerScanner()
    with mock.patch.object(
        LinuxServerScanner, "_parse_sshd_config", return_value={
            "PermitRootLogin": "no", "PasswordAuthentication": "no",
        }
    ):
        findings = scanner._check_ssh_hardening()
    assert len(findings) == 1
    assert findings[0]["severity"] == "INFO"


# --------------------------------------------------------------------------- #
# Dangerous ports
# --------------------------------------------------------------------------- #


def test_dangerous_ports_flags_public_postgres():
    scanner = LinuxServerScanner()
    with mock.patch.object(
        LinuxServerScanner, "_list_listeners",
        return_value=[(5432, "0.0.0.0", "tcp"), (631, "127.0.0.1", "tcp")],
    ):
        findings = scanner._check_dangerous_ports()
    high = [f for f in findings if f["severity"] == "HIGH"]
    assert len(high) == 1
    assert high[0]["port"] == 5432


def test_dangerous_ports_clean_when_loopback_only():
    scanner = LinuxServerScanner()
    with mock.patch.object(
        LinuxServerScanner, "_list_listeners",
        return_value=[(5432, "127.0.0.1", "tcp")],
    ):
        findings = scanner._check_dangerous_ports()
    assert all(f["severity"] == "INFO" for f in findings)


# --------------------------------------------------------------------------- #
# fail2ban
# --------------------------------------------------------------------------- #


def test_fail2ban_not_installed():
    scanner = LinuxServerScanner()
    with mock.patch.object(
        lss, "run_cmd", return_value=CommandResult(127, "", "not found")
    ):
        findings = scanner._check_fail2ban()
    assert findings[0]["severity"] == "HIGH"
    assert "not installed" in findings[0]["description"]


def test_fail2ban_active_with_jail():
    scanner = LinuxServerScanner()
    status_out = "Status\n|- Number of jail: 1\n`- Jail list: sshd\n"

    calls = iter([
        CommandResult(0, "/usr/bin/fail2ban-client", ""),       # command -v
        CommandResult(0, status_out, ""),                        # status
        CommandResult(0, "`- Banned IP list: 1.2.3.4 5.6.7.8", ""),  # status sshd
    ])

    def fake_run(cmd, **kwargs):
        return next(calls)

    with mock.patch.object(lss, "run_cmd", side_effect=fake_run):
        findings = scanner._check_fail2ban()
    assert any("active" in f["description"] for f in findings)
    assert any("sshd" in f["description"] for f in findings)


# --------------------------------------------------------------------------- #
# Docker
# --------------------------------------------------------------------------- #


def test_docker_flags_down_container():
    scanner = LinuxServerScanner()
    out = "messenger-bot\tUp 2 hours\nmessenger-web\tUp 2 hours\n"
    with mock.patch.object(
        lss, "run_cmd", return_value=CommandResult(0, out, "")
    ):
        findings = scanner._check_docker_containers(
            ["messenger-bot", "messenger-web", "messenger-db"]
        )
    high = [f for f in findings if f["severity"] == "HIGH"]
    assert len(high) == 1
    assert "messenger-db" in high[0]["down"]


# --------------------------------------------------------------------------- #
# End-to-end scan()
# --------------------------------------------------------------------------- #


def test_scan_returns_platform_info_on_non_linux():
    scanner = LinuxServerScanner()
    with mock.patch.object(lss.platform, "system", return_value="Windows"):
        result = scanner.scan(".")
    assert result["success"] is True
    assert result["findings"][0]["severity"] == "INFO"
    assert "skipped" in result["findings"][0]["description"]


def test_scan_aggregates_findings_on_linux():
    """Stub every I/O layer and confirm the orchestrator wires things up."""
    scanner = LinuxServerScanner()
    with mock.patch.object(lss.platform, "system", return_value="Linux"), \
         mock.patch.object(LinuxServerScanner, "_check_ssh_hardening", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_fail2ban", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_dangerous_ports", return_value=[]), \
         mock.patch.object(
             LinuxServerScanner, "_check_bruteforce",
             return_value=[{"type": "bruteforce", "severity": "CRITICAL"}],
         ), \
         mock.patch.object(LinuxServerScanner, "_check_authorized_keys", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_suid_binaries", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_process_status", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_docker_containers", return_value=[]), \
         mock.patch.object(LinuxServerScanner, "_check_resources", return_value=[]):
        result = scanner.scan(".")

    assert result["success"] is True
    assert result["total_findings"] == 1
    assert result["severity_count"]["CRITICAL"] == 1


# --------------------------------------------------------------------------- #
# Factory registration
# --------------------------------------------------------------------------- #


def test_factory_registers_linux_scanner():
    from src.scanners.scanner_factory import ScannerFactory

    scanners = ScannerFactory.get_available_scanners()
    assert "linux" in scanners
    instance = ScannerFactory.create_scanner("linux")
    assert instance.__class__.__name__ == "LinuxServerScanner"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Linux Server Security Scanner for SAFEX.

This scanner turns SAFEX from a passive "thermometer" into a real detector.
It performs the checks that the legacy daily script was missing:

* SSH hardening (PasswordAuthentication, PermitRootLogin)
* fail2ban presence, active state, and ban count for the last 24h
* dangerous publicly-bound ports (PostgreSQL, Redis, CUPS, MySQL, MongoDB, ...)
* brute-force analysis of the FULL auth.log (not just ``tail -100``)
* authorized_keys audit
* unknown SUID binaries
* precise process detection that ignores zombie/defunct wrappers
  (fixes the ``pgrep -f server_forever`` false-positive)
* Docker container liveness
* resource health (RAM, disk, UFW)

Every external interaction goes through :func:`src.utils.cmd.run_cmd` so the
scanner is fully deterministic under test (the subprocess layer is mocked).
On non-Linux hosts the scan returns a single INFO finding so the test-suite
stays green on Windows CI.
"""

from __future__ import annotations

import platform
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..config.settings import Settings
from ..utils.cmd import read_file_lines, run_cmd
from ..utils.logger import get_logger
from .base_scanner import BaseScanner

logger = get_logger(__name__)

# Brute-force severity ladder. Evaluated from hardest to softest so the first
# matching threshold wins. 3950 failed logins -> CRITICAL (the original bug
# capped severity at HIGH and only ever saw ``tail -100``).
FAILED_LOGIN_THRESHOLDS: List[Tuple[int, str]] = [
    (1000, "CRITICAL"),
    (200, "HIGH"),
    (50, "MEDIUM"),
    (10, "LOW"),
]

# Ports that must never be exposed on a public interface. The legacy scanner
# ignored these entirely, leaving PostgreSQL/Redis/CUPS wide open.
DANGEROUS_PORTS: Dict[int, str] = {
    23: "Telnet (cleartext)",
    21: "FTP",
    5432: "PostgreSQL",
    6379: "Redis",
    3306: "MySQL/MariaDB",
    27017: "MongoDB",
    9200: "Elasticsearch",
    11211: "Memcached",
    631: "CUPS (printing)",
    2049: "NFS",
    445: "SMB",
}

# SUID binaries considered legitimate on a stock Debian/Ubuntu install.
# Anything outside this set is surfaced for review.
SUID_WHITELIST: frozenset[str] = frozenset(
    {
        "/usr/bin/sudo",
        "/usr/bin/su",
        "/usr/bin/passwd",
        "/usr/bin/chsh",
        "/usr/bin/chfn",
        "/usr/bin/newgrp",
        "/usr/bin/gpasswd",
        "/usr/bin/mount",
        "/usr/bin/umount",
        "/usr/bin/pkexec",
        "/usr/lib/dbus-1.0/dbus-daemon-launch-helper",
        "/usr/lib/openssh/ssh-keysign",
        "/usr/lib/policykit-1/polkit-agent-helper-1",
        "/usr/sbin/unix_chkpwd",
        "/bin/su",
        "/bin/mount",
        "/bin/umount",
        "/bin/ping",
        "/usr/bin/ping",
    }
)

# Regex for a single SSH "Failed password" event.
_FAILED_PASSWORD_RE = re.compile(r"Failed password")
# Captures the timestamp prefix of a typical syslog line, e.g.
# "Jun 21 03:00:01 host sshd[123]: ...". Used to filter the last 24h.
_SYSLOG_TS_RE = re.compile(r"^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})")

_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def severity_for_failed_logins(count: int) -> str:
    """Map a failed-login count to a severity string (INFO when below LOW)."""
    for threshold, sev in FAILED_LOGIN_THRESHOLDS:
        if count >= threshold:
            return sev
    return "INFO"


class LinuxServerScanner(BaseScanner):
    """Deep Linux host security scanner."""

    def __init__(self, config: Optional[Settings] = None):
        super().__init__(config)
        self._now: Callable[[], datetime] = datetime.now

    def get_name(self) -> str:
        return "Linux Server Security Scanner"

    def scan(
        self, target: str, options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run every Linux host check and aggregate findings.

        ``options`` may carry ``docker_containers`` (list of names that must be
        up) and ``service_process`` (executable name to verify, e.g.
        ``server_forever``). Both default to sensible values.
        """
        options = options or {}
        expected_containers = options.get(
            "docker_containers", ["messenger-bot", "messenger-web", "messenger-db"]
        )
        service_process = options.get("service_process", "server_forever")
        auth_log = options.get("auth_log", "/var/log/auth.log")

        findings: List[Dict[str, Any]] = []

        if platform.system() != "Linux":
            findings.append(
                {
                    "type": "platform",
                    "severity": "INFO",
                    "description": (
                        "Linux host checks skipped on %s" % platform.system()
                    ),
                }
            )
        else:
            findings.extend(self._check_ssh_hardening())
            findings.extend(self._check_fail2ban())
            findings.extend(self._check_dangerous_ports())
            findings.extend(self._check_bruteforce(auth_log))
            findings.extend(self._check_authorized_keys())
            findings.extend(self._check_suid_binaries())
            findings.extend(self._check_process_status(service_process))
            findings.extend(self._check_docker_containers(expected_containers))
            findings.extend(self._check_resources())

        result = {
            "success": True,
            "target": target,
            "scanner": self.get_name(),
            "system_info": {"os": platform.system(), "hostname": platform.node()},
            "findings": findings,
            "total_findings": len(findings),
            "severity_count": self._count_by_severity(findings),
        }
        self.scan_results.append(result)
        return result

    # ------------------------------------------------------------------ SSH

    def _check_ssh_hardening(self) -> List[Dict[str, Any]]:
        """Verify sshd_config hardening options."""
        findings: List[Dict[str, Any]] = []
        config = self._parse_sshd_config("/etc/ssh/sshd_config")

        permit_root = config.get("PermitRootLogin", "yes").lower()
        if permit_root not in ("no", "prohibit-password", "without-password"):
            findings.append(
                {
                    "type": "ssh_hardening",
                    "severity": "HIGH",
                    "description": (
                        "PermitRootLogin is '%s' — should be 'no'" % permit_root
                    ),
                    "evidence": "PermitRootLogin %s" % permit_root,
                    "recommendation": "Set 'PermitRootLogin no' and reload sshd",
                }
            )

        pwd_auth = config.get("PasswordAuthentication", "yes").lower()
        if pwd_auth != "no":
            findings.append(
                {
                    "type": "ssh_hardening",
                    "severity": "HIGH",
                    "description": (
                        "PasswordAuthentication is '%s' — brute-force possible"
                        % pwd_auth
                    ),
                    "evidence": "PasswordAuthentication %s" % pwd_auth,
                    "recommendation": (
                        "Use SSH keys and set 'PasswordAuthentication no'"
                    ),
                }
            )

        if not findings:
            findings.append(
                {
                    "type": "ssh_hardening",
                    "severity": "INFO",
                    "description": "SSH hardening options look correct",
                }
            )
        return findings

    @staticmethod
    def _parse_sshd_config(path: str) -> Dict[str, str]:
        """Parse sshd_config into an option dict honoring Match-free semantics.

        The last active (non-commented) directive wins, mirroring sshd itself.
        Include files are not followed — this is a static audit, not a full
        ``sshd -T`` substitution. Callers may inject a real ``sshd -T`` output
        via monkeypatching the path argument in tests.
        """
        result: Dict[str, str] = {}
        for line in read_file_lines(path):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split(None, 1)
            if len(parts) != 2:
                continue
            key, value = parts
            result[key] = value
        return result

    # -------------------------------------------------------------- fail2ban

    def _check_fail2ban(self) -> List[Dict[str, Any]]:
        """Confirm fail2ban is installed, active, and banning attackers."""
        findings: List[Dict[str, Any]] = []

        which = run_cmd(["command", "-v", "fail2ban-client"], shell=True)
        if which.returncode != 0:
            findings.append(
                {
                    "type": "fail2ban",
                    "severity": "HIGH",
                    "description": "fail2ban is not installed",
                    "recommendation": "apt install fail2ban && systemctl enable --now fail2ban",
                }
            )
            return findings

        status = run_cmd(["fail2ban-client", "status"], shell=False)
        # A zero return code means the daemon answered; if it were down the
        # client would exit non-zero. Do NOT look for the word "running" —
        # the status payload never contains it.
        if status.returncode != 0:
            findings.append(
                {
                    "type": "fail2ban",
                    "severity": "HIGH",
                    "description": "fail2ban installed but daemon not responding",
                    "recommendation": "systemctl enable --now fail2ban",
                }
            )
            return findings

        jails = self._extract_jails(status.stdout)
        total_banned = 0
        for jail in jails:
            banned = self._jail_banned_count(jail)
            total_banned += banned
            if banned > 0:
                findings.append(
                    {
                        "type": "fail2ban",
                        "severity": "LOW" if banned < 50 else "MEDIUM",
                        "description": "Jail '%s' currently bans %d IPs" % (jail, banned),
                    }
                )

        findings.append(
            {
                "type": "fail2ban",
                "severity": "INFO",
                "description": "fail2ban active with %d jail(s), %d banned IP(s)"
                % (len(jails), total_banned),
            }
        )
        return findings

    @staticmethod
    def _extract_jails(status_output: str) -> List[str]:
        """Pull jail names out of ``fail2ban-client status`` output."""
        match = re.search(r"Jail list:\s*(.+)", status_output)
        if not match:
            return []
        return [j.strip() for j in match.group(1).split(",") if j.strip()]

    def _jail_banned_count(self, jail: str) -> int:
        """Return the number of currently-banned IPs for a jail."""
        res = run_cmd(["fail2ban-client", "status", jail], shell=False)
        match = re.search(r"Banned IP list:\s*(\S.*)", res.stdout)
        if not match:
            return 0
        IPs = [ip for ip in re.split(r"[\s,]+", match.group(1).strip()) if ip]
        return len(IPs)

    # -------------------------------------------------------- dangerous ports

    def _check_dangerous_ports(self) -> List[Dict[str, Any]]:
        """Flag dangerous services listening on a public interface."""
        findings: List[Dict[str, Any]] = []
        listeners = self._list_listeners()
        public_bindings: List[Tuple[int, str]] = []

        for port, bind_addr, service in listeners:
            if port not in DANGEROUS_PORTS:
                continue
            if self._is_public_bind(bind_addr):
                public_bindings.append((port, service))

        for port, service in public_bindings:
            findings.append(
                {
                    "type": "dangerous_port",
                    "severity": "HIGH",
                    "description": "%s (port %d) bound to a public interface"
                    % (service, port),
                    "port": port,
                    "recommendation": "Bind to 127.0.0.1 or restrict with UFW",
                }
            )

        if not public_bindings:
            findings.append(
                {
                    "type": "dangerous_port",
                    "severity": "INFO",
                    "description": "No dangerous ports exposed publicly",
                }
            )
        return findings

    @staticmethod
    def _is_public_bind(bind_addr: str) -> bool:
        """True when the address indicates a public/all-interfaces bind."""
        addr = bind_addr.strip().strip("[]").lower()
        if addr in ("0.0.0.0", "::", "*", ":::", ""):
            return True
        if addr == "127.0.0.1" or addr == "::1" or addr == "localhost":
            return False
        # Anything else is a concrete address — treat as public for safety.
        return True

    def _list_listeners(self) -> List[Tuple[int, str, str]]:
        """Return ``(port, bind_addr, service)`` tuples for TCP listeners.

        Prefers ``ss`` (present on all modern systemd hosts) and falls back to
        ``netstat``. Both are parsed defensively.
        """
        out = run_cmd(["ss", "-tlnH"], shell=False)
        rows: List[Tuple[int, str, str]] = []
        if out.returncode == 0:
            for line in out.stdout.splitlines():
                cols = line.split()
                if len(cols) < 4:
                    continue
                local = cols[3]
                port = self._parse_port(local)
                addr = self._parse_addr(local)
                if port:
                    rows.append((port, addr, "tcp"))
        else:
            out = run_cmd(["netstat", "-tln"], shell=False)
            for line in out.stdout.splitlines()[2:]:
                cols = line.split()
                if len(cols) < 4 or cols[5] != "LISTEN":
                    continue
                local = cols[3]
                port = self._parse_port(local)
                addr = self._parse_addr(local)
                if port:
                    rows.append((port, addr, "tcp"))
        return rows

    @staticmethod
    def _parse_port(local: str) -> Optional[int]:
        """Extract the numeric port from an ``ss``/``netstat`` local address."""
        if ":" not in local:
            return None
        tail = local.rsplit(":", 1)[-1]
        try:
            return int(tail)
        except ValueError:
            return None

    @staticmethod
    def _parse_addr(local: str) -> str:
        """Extract the bind address from an ``ss``/``netstat`` local address."""
        if ":" not in local:
            return local
        return local.rsplit(":", 1)[0]

    # ----------------------------------------------------------- brute force

    def _check_bruteforce(self, auth_log: str) -> List[Dict[str, Any]]:
        """Count failed SSH logins across the FULL auth.log + rotations.

        This fixes the core bug: the old script only read ``tail -100`` once a
        day, so a 3950-attempt attack was invisible. We now read the current
        file and every rotated sibling (``auth.log.1``, ``auth.log.2.gz`` …)
        and count events from the last 24 hours when timestamps allow it.
        """
        findings: List[Dict[str, Any]] = []
        lines = self._collect_auth_lines(auth_log)
        recent = self._filter_last_24h(lines)
        count = sum(1 for line in recent if _FAILED_PASSWORD_RE.search(line))
        severity = severity_for_failed_logins(count)

        description = "%d failed-login events in the last 24h" % count
        findings.append(
            {
                "type": "bruteforce",
                "severity": severity,
                "description": description,
                "failed_logins_24h": count,
                "scanned_lines": len(lines),
                "recommendation": (
                    "Ensure fail2ban ssh jail is active and review sshd_config"
                    if count >= 10
                    else None
                ),
            }
        )
        return findings

    def _collect_auth_lines(self, auth_log: str) -> List[str]:
        """Read the auth.log plus its rotated siblings (plain or gzipped)."""
        lines: List[str] = []
        lines.extend(read_file_lines(auth_log))

        base = Path(auth_log)
        parent = base.parent
        stem = base.name

        # Plain rotations: auth.log.1, auth.log.2 ...
        for rotated in sorted(parent.glob("%s.*" % stem)):
            suffix = rotated.suffix.lower()
            if suffix == ".gz":
                lines.extend(self._read_gz(str(rotated)))
            else:
                lines.extend(read_file_lines(str(rotated)))
        return lines

    @staticmethod
    def _read_gz(path: str) -> List[str]:
        """Read a gzip-compressed rotated log."""
        try:
            import gzip

            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
                return fh.read().splitlines()
        except Exception as exc:  # pragma: no cover - defensive
            logger.debug("Cannot read gz %s: %s", path, exc)
            return []

    def _filter_last_24h(self, lines: List[str]) -> List[str]:
        """Keep only syslog lines timestamped within the last 24 hours.

        Falls back to returning all lines if timestamp parsing fails for the
        majority of entries — never silently drops evidence.
        """
        if not lines:
            return []

        now = self._now()
        cutoff = now - timedelta(hours=24)
        kept: List[str] = []
        parsed = 0

        for line in lines:
            ts = self._parse_syslog_ts(line, now)
            if ts is None:
                continue
            parsed += 1
            if ts >= cutoff:
                kept.append(line)

        # If almost nothing parsed, the file likely lacks standard timestamps;
        # keep every line so we never under-report an attack.
        if parsed < max(1, len(lines) // 10):
            return lines
        return kept

    def _parse_syslog_ts(self, line: str, now: datetime) -> Optional[datetime]:
        """Parse a ``Mon DD HH:MM:SS`` syslog prefix into a real datetime."""
        match = _SYSLOG_TS_RE.match(line)
        if not match:
            return None
        mon_name, day, hh, mm, ss = match.groups()
        month = _MONTHS.get(mon_name)
        if not month:
            return None
        try:
            ts = datetime(now.year, month, int(day), int(hh), int(mm), int(ss))
        except ValueError:
            return None
        # Handle year rollover (December logs read in January).
        if ts.month > now.month:
            ts = ts.replace(year=now.year - 1)
        return ts

    # ------------------------------------------------------- authorized_keys

    def _check_authorized_keys(self) -> List[Dict[str, Any]]:
        """Audit every user's authorized_keys for quantity and weak perms."""
        findings: List[Dict[str, Any]] = []
        home_root = Path("/home")
        if not home_root.is_dir():
            return findings

        for home in home_root.iterdir():
            if not home.is_dir():
                continue
            keys_file = home / ".ssh" / "authorized_keys"
            if not keys_file.is_file():
                continue
            try:
                content = keys_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            key_count = sum(
                1 for line in content.splitlines()
                if line.strip() and not line.strip().startswith("#")
            )
            if key_count == 0:
                continue

            try:
                mode = keys_file.stat().st_mode & 0o777
            except OSError:
                mode = 0o644
            weak_perms = bool(mode & 0o022)

            sev = "LOW"
            if key_count > 5:
                sev = "MEDIUM"
            if weak_perms:
                sev = "MEDIUM"

            findings.append(
                {
                    "type": "authorized_keys",
                    "severity": sev,
                    "description": "User '%s' has %d authorized key(s)" % (home.name, key_count),
                    "user": home.name,
                    "key_count": key_count,
                    "weak_permissions": weak_perms,
                    "recommendation": (
                        "chmod 600 authorized_keys" if weak_perms else None
                    ),
                }
            )
        return findings

    # ---------------------------------------------------------- SUID binaries

    def _check_suid_binaries(self) -> List[Dict[str, Any]]:
        """Surface SUID binaries that are not on the known-good whitelist."""
        findings: List[Dict[str, Any]] = []
        out = run_cmd(["find", "/", "-xdev", "-perm", "-4000", "-type", "f"])
        if out.returncode != 0:
            return findings

        unknown = [
            path.strip()
            for path in out.stdout.splitlines()
            if path.strip() and path.strip() not in SUID_WHITELIST
        ]
        if unknown:
            findings.append(
                {
                    "type": "suid_binary",
                    "severity": "MEDIUM",
                    "description": "%d non-whitelisted SUID binary/binaries found"
                    % len(unknown),
                    "binaries": unknown[:50],
                    "recommendation": "Review each entry; remove SUID bit if unintended",
                }
            )
        else:
            findings.append(
                {
                    "type": "suid_binary",
                    "severity": "INFO",
                    "description": "No unexpected SUID binaries",
                }
            )
        return findings

    # ------------------------------------------- process status (zombie-safe)

    def _check_process_status(self, process_name: str) -> List[Dict[str, Any]]:
        """Verify a service is running WITHOUT matching zombie wrappers.

        Fixes the bug where ``pgrep -f server_forever`` matched the parent
        bash wrapper (PID 99832) left behind after killing the real parser,
        producing a false "UNIPARSER is running". Instead we walk ``/proc``,
        read each task's state, and ignore zombies (state ``Z``) and any
        process whose executable name does not equal the target exactly.
        """
        findings: List[Dict[str, Any]] = []
        pids = self._find_live_processes(process_name)

        if pids:
            findings.append(
                {
                    "type": "process_status",
                    "severity": "INFO",
                    "description": "Process '%s' is running (PIDs: %s)"
                    % (process_name, ", ".join(str(p) for p in pids)),
                    "pids": pids,
                }
            )
        else:
            findings.append(
                {
                    "type": "process_status",
                    "severity": "HIGH",
                    "description": "Process '%s' is NOT running" % process_name,
                    "recommendation": "Start the service and verify it stays up",
                }
            )
        return findings

    @staticmethod
    def _find_live_processes(target: str) -> List[int]:
        """Return PIDs of non-zombie processes whose comm == target.

        Uses ``/proc`` directly to avoid ``pgrep -f`` substring false-positives.
        A process is counted only when:
        * ``/proc/<pid>/comm`` equals ``target`` (exact, not substring), and
        * the task state is not ``Z`` (zombie/defunct).
        """
        pids: List[int] = []
        proc = Path("/proc")
        if not proc.is_dir():
            return pids

        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            pid = int(entry.name)
            stat_path = entry / "stat"
            comm_path = entry / "comm"
            try:
                stat_text = stat_path.read_text(errors="replace")
                comm = comm_path.read_text(errors="replace").strip()
            except (FileNotFoundError, ProcessLookupError, OSError):
                continue

            state = LinuxServerScanner._proc_state(stat_text)
            if state == "Z":
                continue
            if comm == target:
                pids.append(pid)
        return pids

    @staticmethod
    def _proc_state(stat_text: str) -> str:
        """Extract the task state char from a ``/proc/<pid>/stat`` line.

        The comm field is wrapped in parentheses and may contain spaces, so we
        parse from the last closing paren rather than splitting naively.
        """
        rparen = stat_text.rfind(")")
        if rparen == -1:
            return "?"
        rest = stat_text[rparen + 1:].split()
        if len(rest) >= 1:
            return rest[0]
        return "?"

    # ------------------------------------------------------- docker containers

    def _check_docker_containers(self, expected: List[str]) -> List[Dict[str, Any]]:
        """Confirm each expected container is in 'running' state."""
        findings: List[Dict[str, Any]] = []
        running = self._running_containers()
        down = [name for name in expected if name not in running]

        if down:
            findings.append(
                {
                    "type": "docker",
                    "severity": "HIGH",
                    "description": "%d container(s) not running: %s"
                    % (len(down), ", ".join(down)),
                    "down": down,
                    "recommendation": "docker compose up -d",
                }
            )
        else:
            findings.append(
                {
                    "type": "docker",
                    "severity": "INFO",
                    "description": "All %d expected container(s) running" % len(expected),
                }
            )
        return findings

    @staticmethod
    def _running_containers() -> List[str]:
        """Return names of running containers via the Docker CLI."""
        out = run_cmd(
            ["docker", "ps", "--format", "{{.Names}}\t{{.Status}}"], shell=False
        )
        if out.returncode != 0:
            return []
        names: List[str] = []
        for line in out.stdout.splitlines():
            cols = line.split("\t")
            if len(cols) < 2:
                continue
            status = cols[1].lower()
            if status.startswith("up"):
                names.append(cols[0].strip())
        return names

    # -------------------------------------------------------------- resources

    def _check_resources(self) -> List[Dict[str, Any]]:
        """Check RAM, disk usage, and UFW firewall state."""
        findings: List[Dict[str, Any]] = []
        findings.extend(self._check_memory())
        findings.extend(self._check_disk())
        findings.extend(self._check_ufw())
        return findings

    def _check_memory(self) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        out = run_cmd(["free", "-m"], shell=False)
        if out.returncode != 0:
            return findings
        lines = out.stdout.splitlines()
        for line in lines:
            if line.lower().startswith("mem:"):
                parts = line.split()
                if len(parts) >= 3:
                    total = int(parts[1])
                    avail = int(parts[6]) if len(parts) >= 7 else int(parts[3])
                    if total:
                        used_pct = round(100 * (total - avail) / total)
                        sev = "HIGH" if used_pct >= 90 else ("MEDIUM" if used_pct >= 75 else "INFO")
                        findings.append(
                            {
                                "type": "memory",
                                "severity": sev,
                                "description": "Memory usage: %d%% (%d/%d MB)"
                                % (used_pct, total - avail, total),
                            }
                        )
        return findings

    def _check_disk(self) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        out = run_cmd(["df", "-h", "/"], shell=False)
        if out.returncode != 0:
            return findings
        lines = out.stdout.splitlines()
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 5 and parts[4].rstrip("%").isdigit():
                used_pct = int(parts[4].rstrip("%"))
                sev = "HIGH" if used_pct >= 90 else ("MEDIUM" if used_pct >= 80 else "INFO")
                findings.append(
                    {
                        "type": "disk",
                        "severity": sev,
                        "description": "Root filesystem usage: %d%%" % used_pct,
                    }
                )
        return findings

    def _check_ufw(self) -> List[Dict[str, Any]]:
        findings: List[Dict[str, Any]] = []
        out = run_cmd(["ufw", "status"], shell=False)
        if out.returncode != 0:
            findings.append(
                {
                    "type": "firewall",
                    "severity": "MEDIUM",
                    "description": "UFW not available or not installed",
                }
            )
            return findings
        if "Status: active" in out.stdout:
            findings.append(
                {
                    "type": "firewall",
                    "severity": "INFO",
                    "description": "UFW firewall is active",
                }
            )
        else:
            findings.append(
                {
                    "type": "firewall",
                    "severity": "HIGH",
                    "description": "UFW firewall is NOT active",
                    "recommendation": "ufw enable",
                }
            )
        return findings

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _count_by_severity(findings: List[Dict[str, Any]]) -> Dict[str, int]:
        count: Dict[str, int] = {}
        for finding in findings:
            sev = finding.get("severity", "LOW")
            count[sev] = count.get(sev, 0) + 1
        return count

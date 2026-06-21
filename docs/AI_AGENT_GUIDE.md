# SAFEX — Guide for AI Agents

This document helps AI coding agents understand the SAFEX codebase quickly and make correct contributions.

---

## Quick Reference

| What | Where |
|---|---|
| Entry point | `safex.py` → calls `src.cli.cli_main.main()` |
| All settings | `src/utils/config.py` (pydantic `Settings` class) |
| Logger | `src/utils/logger.py` → `get_logger("name")` |
| Scanner registry | `src/scanners/scanner_factory.py` → `ScannerFactory.create_scanner("type")` |
| Bot security | `src/bots_security/` (6 modules) |
| Knowledge base data | `knowledge_base/*.json` and `knowledge_base/*.yaml` |
| Tests | `tests/test_*.py` |
| Podman templates | `configs/podman/` |

---

## Code Conventions

1. **Imports**: All internal imports are relative within `src/` package. External entry via `safex.py`.
2. **Config**: Always use `from ..config.settings import Settings` or `from ..utils.config import settings` (the global instance).
3. **Logging**: Always use `from ..utils.logger import get_logger` → `logger = get_logger(__name__)`.
4. **Scanners**: Extend `BaseScanner` (abstract). Implement `scan()` and `get_name()`. Register in `ScannerFactory._scanners`.
5. **Tools**: Extend `BaseTool` (abstract). Implement `execute()`, `get_name()`, `is_available()`. Register in `ToolFactory._tools`.
6. **No comments in code** unless explicitly requested by user.
7. **Refactor always** — do not expand files infinitely (per AGENTS.md).

---

## Module Map

```
src/
├── cli/             # CLI — argparse-based, subcommands
│   └── cli_main.py  # ALL CLI commands defined here (validate, scan, report, status, list, bot-scan, bot-audit, bot-deploy)
├── config/          # Re-exports Settings from utils/config.py
├── core/            # Validation engine + ownership validator
├── bots_security/   # Bot security (NEW module)
│   ├── models.py    # Dataclasses: BotSecurityFinding, BotAuditResult, enums
│   ├── bot_scanner.py    # BotScanner(BaseScanner) — main scanner
│   ├── webhook_guard.py  # WebhookGuard — webhook security checks
│   ├── token_guard.py    # TokenGuard — token leak detection
│   ├── audit_checklist.py # AuditChecklist — security checklists
│   └── podman_templates.py # PodmanTemplates — deployment config generator
├── safety/          # SafetyManager, SafetyLevel, monitor, progressive exec
├── scanners/        # BaseScanner, ScannerFactory, ConfigScanner, CodeScanner, SystemScanner
├── tools/           # BaseTool, ToolFactory, ToolManager
├── reporting/       # ReportGenerator, formatters
├── knowledge_base/  # KnowledgeBase manager (reads from knowledge_base/ data files)
├── autofix/         # AutoFixEngine
├── api/             # FastAPI app factory
├── queue/           # Celery config
├── tui/             # Text UI (urwid)
├── validation/      # Validation utilities, email handler
├── i18n/            # TranslationManager (10 languages)
└── utils/           # config.py (Settings), logger.py, helpers.py, exceptions.py
```

---

## How to Add Features

### Add a new scanner type

1. Create `src/scanners/your_scanner.py`:
```python
from .base_scanner import BaseScanner
from ..utils.logger import get_logger
logger = get_logger(__name__)

class YourScanner(BaseScanner):
    def get_name(self) -> str:
        return "Your Scanner Name"

    def scan(self, target: str, options=None) -> dict:
        return {"success": True, "findings": [], "total_findings": 0, "severity_count": {}}
```

2. Register in `src/scanners/scanner_factory.py`:
```python
from .your_scanner import YourScanner
_scanners = { ..., "your_type": YourScanner }
```

3. Add CLI choice in `src/cli/cli_main.py` scan parser.

### Add a new bot platform

1. Add to `PlatformType` enum in `src/bots_security/models.py`.
2. Add token regex in `src/bots_security/bot_scanner.py` (`_TOKEN_PATTERNS`).
3. Add token regex in `src/bots_security/token_guard.py` (`PLATFORM_TOKEN_REGEX`).
4. Add rules to `knowledge_base/bot_security_rules.yaml`.
5. Add entry to `knowledge_base/bot_vulnerabilities.json`.

### Add a new vulnerability pattern

1. Add to scanner's pattern list (e.g., `_check_*` methods in `CodeScanner` or `BotScanner`).
2. Add rule to `knowledge_base/security_rules.yaml`.
3. Add entry to `knowledge_base/vulnerabilities.json`.

---

## Important Files (Do NOT modify without reason)

- `safex.py` — entry point, only imports `src.cli.cli_main.main()`
- `src/utils/config.py` — all settings live here
- `src/scanners/base_scanner.py` — abstract interface for all scanners
- `src/scanners/scanner_factory.py` — scanner registry
- `knowledge_base/vulnerabilities.json` — vulnerability database
- `knowledge_base/bot_vulnerabilities.json` — bot vulnerability database

---

## Testing Patterns

Tests use `pytest` with `tempfile` for file-based tests:

```python
@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

def test_my_scanner(tmp_dir):
    code_file = tmp_dir / "test.py"
    code_file.write_text("code here", encoding="utf-8")
    scanner = MyScanner()
    result = scanner.scan(str(tmp_dir))
    assert result["success"]
    assert result["total_findings"] >= 1
```

Run tests: `pytest tests/ -v`

---

## Architecture Patterns

### Factory Pattern (Scanners, Tools)
```python
scanner = ScannerFactory.create_scanner("bot")
# Returns instance of BotScanner
```

### Lazy Loading (BotScanner)
BotScanner is loaded on first use to avoid import overhead:
```python
@classmethod
def _ensure_bot_scanner(cls):
    if "bot" not in cls._scanners:
        from ..bots_security.bot_scanner import BotScanner
        cls._scanners["bot"] = BotScanner
```

### Settings Singleton
```python
from src.utils.config import settings  # global instance
# Or create fresh: Settings()
```

### Dataclass Models (Bot Security)
```python
finding = BotSecurityFinding(
    category=FindingCategory.TOKEN_LEAK,
    risk_level=RiskLevel.CRITICAL,
    title="Leaked Token",
    description="...",
)
audit = BotAuditResult(target="path", platform=PlatformType.TELEGRAM)
audit.add_finding(finding)
print(audit.risk_score, audit.passed, audit.severity_count())
```

---

## Common Pitfalls

1. **Path handling**: Always use `Path()` from pathlib. Never hardcode `/` or `\\`.
2. **Encoding**: Always specify `encoding="utf-8"` when reading/writing files.
3. **Scanners return dicts**: Not objects. Format: `{"success": bool, "findings": list, "total_findings": int, "severity_count": dict}`.
4. **Bot scanner findings**: Use `BotSecurityFinding` dataclass, not raw dicts. Call `finding.to_dict()` for serialization.
5. **WebhookGuard**: Call `audit_webhook_code(code, file_path, platform)`, returns `List[BotSecurityFinding]`.
6. **TokenGuard**: Call `scan_file(path)` or `scan_directory(path)`, returns `List[BotSecurityFinding]`.
7. **Podman, not Docker**: All container files and documentation reference Podman. Never suggest Docker.

---

## Key Numbers

| Metric | Count |
|---|---|
| Source modules | 17 directories under `src/` |
| Scanner types | 4 (config, code, system, bot) |
| Bot platforms | 7 (Telegram, Discord, Slack, VK, Viber, WhatsApp, Generic) |
| Finding categories | 13 |
| General vulnerabilities | 8 (VULN-001..VULN-008) |
| Bot vulnerabilities | 12 (BOT-001..BOT-012) |
| Security rules | 7 general + 12 bot = 19 |
| Languages | 10 |
| Tests | 47 |
| Bot security tests | 31 |

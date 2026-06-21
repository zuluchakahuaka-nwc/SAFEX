# SAFEX Architecture Guide

## Overview

SAFEX (Security Audit Framework for Enhanced Protection) is a modular Python security framework. It provides scanners, validators, safety management, and specialized bot security — all accessible via CLI, Python API, or REST API.

---

## Architecture Principles

| Principle | Description |
|---|---|
| **Plugin architecture** | Scanners and tools are registered via Factory pattern. Add new scanners without modifying existing code. |
| **Safety-first** | Every operation goes through SafetyManager. 4 levels: discovery → safe → moderate → aggressive. |
| **i18n native** | All user-facing strings go through TranslationManager. 10 languages built-in. |
| **Knowledge-driven** | Vulnerability rules, fix recommendations, and patterns live in `knowledge_base/` data files, not in code. |
| **Containerized** | Full Podman support. Deployment templates generate secure containers out of the box. |

---

## Module Dependency Graph

```
                        safex.py (entry point)
                             │
                        cli/cli_main.py
                             │
         ┌───────────┬───────┼───────────┬──────────────┐
         │           │       │           │              │
    core/        scanners/ safety/   bots_security/  reporting/
    validation   factory   manager   bot_scanner     report_gen
    engine       ├──config  │        webhook_guard   formatters
         │       ├──code    │        token_guard
         │       ├──system  │        audit_checklist
         │       └──bot ────┘        podman_templates
         │                │
         └────────────────┤
                          │
               ┌──────────┼──────────┐
               │          │          │
          utils/config  utils/logger  i18n/
          (Settings)    (get_logger)  translation_manager
               │
          knowledge_base/
          (data files)
```

---

## Data Flow

### Scan Flow

```
User → CLI (cli_main.py) → ScannerFactory.create_scanner(type)
                                │
                          BaseScanner.scan(target, options)
                                │
                    ┌───────────┼───────────┐
                    │           │           │
              ConfigScanner  CodeScanner  BotScanner
              (.yaml/.json)  (.py/.js)    (bot projects)
                    │           │           │
                    └───────────┼───────────┘
                                │
                         ScanResult dict
                         {success, findings, severity_count, ...}
                                │
                    ReportGenerator → JSON/HTML/Markdown/CSV
```

### Bot Security Scan Flow

```
User → bot-scan <path> → BotScanner.scan()
                              │
                   ┌──────────┼──────────────┐
                   │          │              │
            _scan_tokens  _scan_patterns  _scan_webhook_usage
            (TokenGuard)  (eval/injection  (WebhookGuard)
                          /deserialize/
                           secrets/logging)
                   │          │              │
                   └──────────┼──────────────┘
                              │
                       BotAuditResult
                       {findings, risk_score, passed}
                              │
                    AuditChecklist.generate_from_audit()
                    PodmanTemplates.generate_all() (if needed)
```

---

## Core Modules Deep Dive

### 1. Configuration (`src/utils/config.py`)

**Single source of truth** for all settings via pydantic-settings.

```python
from src.utils.config import settings, get_settings

# Access any setting
print(settings.app_name)       # "SAFEX"
print(settings.api_port)       # 8000
print(settings.database_url)   # "postgresql://..."
```

Key settings groups:
- **Application**: name, version, debug, environment
- **Paths**: base_dir, configs_dir, data_dir, reports_dir, knowledge_base_path
- **Database**: PostgreSQL URL, pool settings
- **Redis/Queue**: Celery broker, result backend
- **Security**: secret_key, JWT algorithm, token expiry
- **API**: host, port, workers, CORS origins
- **Rate Limiting**: enabled, requests/period

Settings are loaded from `.env` file automatically.

### 2. Scanners (`src/scanners/`)

**Base class** (`base_scanner.py`):
```python
class BaseScanner(ABC):
    def scan(self, target: str, options: Dict = None) -> Dict[str, Any]: ...
    def get_name(self) -> str: ...
    def validate_target(self, target: str) -> bool: ...
```

**Factory** (`scanner_factory.py`) — register and create scanners:
```python
# Built-in scanners: "config", "code", "system", "bot"
scanner = ScannerFactory.create_scanner("code")
result = scanner.scan("/path/to/file.py")

# Register custom scanner
ScannerFactory.register_scanner("custom", MyCustomScanner)
```

**Available scanners**:

| Scanner | Type | What it scans |
|---|---|---|
| ConfigScanner | `config` | YAML, JSON, XML, INI files — insecure defaults, exposed secrets, weak encryption, permissions |
| CodeScanner | `code` | Python, JS, TS, Java, C/C++, Go, Ruby, PHP, Rust — hardcoded secrets, SQL injection, XSS, deserialization, weak crypto, command injection |
| SystemScanner | `system` | Windows system — OS updates, antivirus, firewall, user accounts, open ports, services |
| BotScanner | `bot` | Bot projects — token leaks, eval/exec, command injection, deserialization, rate limiting, webhook security, file upload issues |

### 3. Bot Security (`src/bots_security/`)

#### Models (`models.py`)

```python
class PlatformType(str, Enum):
    TELEGRAM, DISCORD, SLACK, VK, VIBER, WHATSAPP, GENERIC

class FindingCategory(str, Enum):
    TOKEN_LEAK, WEBHOOK_MISCONFIG, INPUT_VALIDATION, FILE_UPLOAD,
    INSECURE_DEPENDENCY, PERMISSION_FLAW, CONTAINER_SECURITY,
    NETWORK_EXPOSURE, LOGGING_LEAK, DESERIALIZATION,
    COMMAND_INJECTION, RATE_LIMITING, SECRET_STORAGE

class RiskLevel(str, Enum):
    INFO, LOW, MEDIUM, HIGH, CRITICAL

@dataclass
class BotSecurityFinding:
    category: FindingCategory
    risk_level: RiskLevel
    title: str
    description: str
    # + location, code_snippet, line_number, recommendation, cwe_id, platform

@dataclass
class BotAuditResult:
    target: str
    platform: PlatformType
    findings: List[BotSecurityFinding]
    risk_score: float    # 0..100
    passed: bool         # True if risk_score < 40
```

#### BotScanner (`bot_scanner.py`)

Inherits from `BaseScanner`. Detects:
- Leaked tokens (Telegram `\d{8,10}:[A-Za-z0-9_-]{33,38}`, Discord, Slack, VK)
- `eval()` / `exec()` usage
- `subprocess` with `shell=True`
- `pickle.loads()`, `yaml.load()` without safe Loader
- Hardcoded passwords, API keys, secret keys, webhook secrets
- Missing rate limiting (handlers without throttle middleware)
- Webhook without HTTPS or secret verification

#### WebhookGuard (`webhook_guard.py`)

Checks 6 aspects of webhook security:
1. HTTPS enforcement (rejects `http://` URLs)
2. Secret token verification (`hmac.compare_digest`)
3. IP allowlist for webhook endpoint
4. Error handling (try/except in handlers)
5. Payload size limits
6. Request timeouts

Generates secure webhook template code.

#### TokenGuard (`token_guard.py`)

Detects leaked tokens in files and directories:
- Platform-specific regex for Telegram, Discord, Slack, VK
- Inline secret detection (hardcoded values in source)
- `.env` file safety (checks .gitignore, validates values)
- Token format validation

#### AuditChecklist (`audit_checklist.py`)

Predefined checklists organized by priority:

| Priority | Checks | Examples |
|---|---|---|
| HIGH (A-001..A-007) | 7 | Token storage, webhook secret, HTTPS, input validation, file upload, container security, network isolation |
| MEDIUM (B-001..B-004) | 4 | Rate limiting, dependency audit, logging, resource limits |
| LOW (C-001..C-002) | 2 | Admin endpoint protection, backup & incident response |

Generates:
- JSON checklist with pass/fail status
- Text report (human-readable)
- 7-step incident response plan

#### PodmanTemplates (`podman_templates.py`)

Generates 5 deployment files:

| File | Purpose |
|---|---|
| `Containerfile` | Non-root user, minimal deps, gunicorn |
| `podman-compose.yml` | Bot + nginx, isolated network, resource limits, read-only FS, no-new-privileges, cap_drop ALL |
| `nginx/nginx.conf` | TLS termination, rate limiting, 2MB body limit, redirect HTTP→HTTPS |
| `systemd/bot.service` | Systemd unit with sandboxing (ProtectSystem, NoNewPrivileges, PrivateTmp) |
| `.env.example` | Template for secrets (never commit) |

### 4. Safety Manager (`src/safety/safety_manager.py`)

```python
sm = SafetyManager()

# Assess risk of an operation
risk = sm.assess_fix_risk("VULN-001", "/path/to/file", "HIGH")
# Returns: {level: "HIGH", vuln_id, target, message}

# Confirm dangerous operation
confirmed = sm.confirm_fix("VULN-001", "/path", "CRITICAL")
# Prompts user for y/N confirmation

# Get emoji for severity
emoji = sm.get_warning_emoji("CRITICAL")  # "🚨"
```

### 5. Validation Engine (`src/core/validation_engine.py`)

```python
engine = ValidationEngine()

# Single target
result = engine.validate_target("/path", method="auto", safety_level="safe")
# Returns: {target, method, safety_level, is_valid, message, timestamp}

# Batch validation
result = engine.validate_batch(["/path1", "/path2"])

# Directory scan
result = engine.validate_directory("/dir", pattern="*.py", recursive=True)

# Export
path = engine.export_results(format="json", output_path="results.json")
```

### 6. Reporting (`src/reporting/`)

```python
from src.reporting.report_generator import ReportGenerator

rg = ReportGenerator()
path = rg.generate_report(data, format="json", output_path="report.json")
# Formats: json, text, html, markdown
```

### 7. Knowledge Base (`knowledge_base/`)

Data files (not code):

| File | Contents |
|---|---|
| `vulnerabilities.json` | 8 general vulnerabilities (VULN-001..VULN-008) — hardcoded passwords, SQL injection, weak crypto, etc. |
| `bot_vulnerabilities.json` | 12 bot-specific vulnerabilities (BOT-001..BOT-012) — token leaks, webhook misconfig, eval RCE, etc. |
| `security_rules.yaml` | 7 general security rules with regex patterns and recommendations |
| `bot_security_rules.yaml` | 12 bot security rules with regex patterns and recommendations |
| `fix_recommendations.json` | Fix recommendations for each vulnerability |

### 8. API (`src/api/app.py`)

FastAPI application factory:
```python
from src.api.app import create_app
app = create_app()
# Run: uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port 8000
```

### 9. CLI (`src/cli/cli_main.py`)

Full command reference:

```
safex validate <target> [--method auto|file_permission|registry|service] [-s safety_level]
safex scan <target> [--scanner auto|config|code|system|vulnerability|network|web|bot]
safex report [--format json|text|html|markdown] [--output file]
safex status
safex list scanners|tools|languages
safex bot-scan <path> [--platform telegram|discord|slack|vk|viber|whatsapp|generic]
safex bot-audit [--platform telegram] [--text] [--output file]
safex bot-deploy [--platform telegram] [--domain bot.example.com] [--output-dir ./bot-deploy]

Global options:
  --language, -l   en|ru|es|fr|de|zh|ja|ar|pt|it
  --safety-level, -s   discovery|safe|moderate|aggressive
  --verbose, -v
```

---

## Extension Points

### Adding a new scanner

1. Create `src/scanners/my_scanner.py`:
```python
from .base_scanner import BaseScanner

class MyScanner(BaseScanner):
    def get_name(self) -> str:
        return "My Custom Scanner"

    def scan(self, target: str, options=None) -> dict:
        return {"success": True, "findings": [], ...}
```

2. Register in `scanner_factory.py`:
```python
_scanners = {
    ...
    "my_scanner": MyScanner,
}
```

3. Add CLI option in `cli_main.py`.

### Adding a new platform to bot security

1. Add platform to `PlatformType` enum in `models.py`.
2. Add token regex to `_TOKEN_PATTERNS` in `bot_scanner.py`.
3. Add token regex to `PLATFORM_TOKEN_REGEX` in `token_guard.py`.
4. Add platform-specific rules to `knowledge_base/bot_security_rules.yaml`.

### Adding a new vulnerability rule

1. Add entry to `knowledge_base/vulnerabilities.json` or `knowledge_base/bot_vulnerabilities.json`.
2. Add detection pattern to `knowledge_base/security_rules.yaml` or `knowledge_base/bot_security_rules.yaml`.
3. Optionally add detection code to the relevant scanner.

---

## Testing

### Test Structure

```
tests/
├── test_basic.py            # Project structure, module imports
├── test_core.py             # ValidationEngine, OwnershipValidator
├── test_safety.py           # SafetyManager, SafetyLevel
├── test_config.py           # Settings
└── test_bots_security.py    # 31 tests covering all bot security components
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific module
pytest tests/test_bots_security.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# In Podman
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ -v
```

---

## Deployment

### Podman (Recommended for Bots)

```bash
# Generate secure deployment templates
python safex.py bot-deploy --platform telegram --domain my.bot.com --output-dir ./my-bot-deploy

# Deploy
cd my-bot-deploy
cp .env.example .env  # Edit with real values
# Add TLS certs to nginx/certs/
podman-compose up -d
```

### Docker (Main Application)

```bash
# Build
podman build -t safex -f docker/Dockerfile .

# Full stack
podman-compose -f docker/docker-compose.yml up -d
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| pydantic-settings for config | Type-safe, env var loading, validation |
| Factory pattern for scanners | Extensible, lazy loading, testable |
| Dataclasses for bot findings | Lightweight, no ORM dependency |
| Lazy import for BotScanner | Avoids circular imports, keeps core lightweight |
| Podman over Docker | Rootless containers, better security, daemonless |
| Knowledge base as data files | Rules can be updated without code changes |
| Safety levels as first-class concept | Prevents accidental damage in production |

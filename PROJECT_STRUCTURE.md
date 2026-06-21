# SAFEX Project Structure

This document describes the complete structure of the SAFEX project.

## Directory Structure

```
SAFEX/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables example
├── SECURITY.md                  # Security guidelines
├── SAFE_TESTING.md             # Safe testing guidelines
├── README_I18N.md              # Internationalization documentation
├── safex.py                    # CLI entry point
├── src/                        # Source code
│   ├── __init__.py
│   ├── cli/                    # Command-line interface
│   │   ├── __init__.py
│   │   ├── cli_main.py         # Main CLI implementation (scan, validate, bot-scan, bot-audit, bot-deploy)
│   │   ├── cli_tui.py          # Text User Interface
│   │   └── cli_validation.py   # Validation commands
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py         # Settings class (re-exports from utils/config.py)
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── validator.py        # Ownership validator
│   │   └── validation_engine.py # Validation engine
│   ├── bots_security/          # Bot security module (NEW)
│   │   ├── __init__.py         # Module exports
│   │   ├── models.py           # Data models (PlatformType, RiskLevel, FindingCategory, etc.)
│   │   ├── bot_scanner.py      # BotSecurityScanner — scans bot source for vulnerabilities
│   │   ├── webhook_guard.py    # WebhookGuard — validates webhook security config
│   │   ├── token_guard.py      # TokenGuard — detects leaked tokens (Telegram, Discord, Slack, VK)
│   │   ├── audit_checklist.py  # AuditChecklist — generates security audit checklists
│   │   └── podman_templates.py # PodmanTemplates — generates secure Podman deployment configs
│   ├── safety/                 # Safety features
│   │   ├── __init__.py
│   │   ├── safety_manager.py   # Safety level manager
│   │   ├── models.py           # Safety data models
│   │   ├── warnings.py         # Warning system
│   │   ├── monitor.py          # Monitoring system
│   │   └── progressive.py      # Progressive execution
│   ├── i18n/                   # Internationalization
│   │   ├── __init__.py
│   │   ├── translator.py       # Translation core
│   │   └── translation_manager.py # Translation manager
│   ├── knowledge_base/         # Vulnerability knowledge base
│   │   ├── __init__.py
│   │   └── knowledge_base.py   # Knowledge base manager
│   ├── autofix/                # Auto-fix functionality
│   │   ├── __init__.py
│   │   └── autofix_engine.py   # Auto-fix engine
│   ├── scanners/               # Security scanners
│   │   ├── __init__.py
│   │   ├── base_scanner.py     # Abstract base class for all scanners
│   │   ├── scanner_factory.py  # Scanner factory (registry + lazy loading)
│   │   ├── config_scanner.py   # Configuration file scanner
│   │   ├── code_scanner.py     # Source code scanner
│   │   ├── system_scanner.py   # System security scanner
│   │   ├── web_scanner.py      # Web application scanner
│   │   ├── vulnerability_scanner.py # Known vulnerability scanner
│   │   └── network_scanner.py  # Network security scanner
│   ├── tools/                  # Security tools
│   │   ├── __init__.py
│   │   ├── base_tool.py        # Abstract base class for all tools
│   │   ├── tool_factory.py     # Tool factory
│   │   └── tool_manager.py     # Tool manager
│   ├── reporting/              # Reporting system
│   │   ├── __init__.py
│   │   ├── report_generator.py # Report generator
│   │   └── formatters.py       # Report formatters (JSON, Text, HTML, Markdown)
│   ├── api/                    # REST API
│   │   ├── __init__.py
│   │   ├── app.py              # FastAPI application factory
│   │   ├── routes/             # API routes
│   │   └── middleware/         # API middleware
│   ├── queue/                  # Task queue
│   │   ├── __init__.py
│   │   └── celery_app.py       # Celery configuration
│   ├── tui/                    # Text User Interface
│   │   ├── __init__.py
│   │   └── main.py             # TUI entry point
│   ├── validation/             # Validation utilities
│   │   ├── __init__.py
│   │   ├── validator.py        # Generic validator
│   │   ├── email_handler.py    # Email handling
│   │   └── models.py           # Validation models
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── config.py           # Settings (pydantic-settings), global `settings` instance
│       ├── logger.py           # Logger factory + LoggerContext
│       ├── helpers.py          # Helper functions
│       └── exceptions.py       # Custom exceptions
├── tests/                      # Tests
│   ├── __init__.py
│   ├── test_basic.py           # Basic integration tests
│   ├── test_core.py            # Core module tests
│   ├── test_safety.py          # Safety module tests
│   ├── test_config.py          # Config module tests
│   └── test_bots_security.py   # Bot security module tests (31 tests)
├── configs/                    # Configuration files
│   └── podman/                 # Podman deployment templates
│       ├── Containerfile       # Secure Containerfile (non-root, Python 3.11)
│       ├── podman-compose.yml  # Podman Compose (bot + nginx)
│       ├── nginx/
│       │   └── nginx.conf      # Nginx reverse proxy config (TLS, rate limit)
│       ├── bot.service         # Systemd unit file
│       └── .env.example        # Environment variables template
├── knowledge_base/             # Knowledge base data
│   ├── vulnerabilities.json    # General vulnerability database (VULN-001..VULN-008)
│   ├── bot_vulnerabilities.json # Bot-specific vulnerability database (BOT-001..BOT-012)
│   ├── fix_recommendations.json # Fix recommendations
│   ├── security_rules.yaml     # General security rules (7 rules)
│   └── bot_security_rules.yaml # Bot security rules (12 rules)
├── docker/                     # Docker/Podman configuration
│   ├── Dockerfile              # Main application Dockerfile
│   ├── docker-compose.yml      # Main docker-compose (postgres, redis, api, celery, nginx)
│   ├── docker-compose.test.yml # Test compose
│   ├── docker-compose.scan.yml # Scan compose
│   └── *.sh / *.bat            # Helper scripts
├── scripts/                    # Installation and setup scripts
│   ├── install.sh              # Linux/macOS install
│   ├── setup.sh                # Linux/macOS setup
│   └── setup.bat               # Windows setup
├── frontend/                   # Frontend (React)
│   ├── package.json
│   └── ...
├── test-targets/               # Test targets for scanning
│   └── vulnerable_app.py       # Vulnerable test application
└── docs/                       # Documentation
    ├── ARCHITECTURE.md          # Architecture deep-dive
    ├── AI_AGENT_GUIDE.md        # Guide for AI agents working with SAFEX
    ├── INSTALLATION_UBUNTU.md   # Ubuntu installation guide
    ├── UBUNTU_INSTALL.md        # Ubuntu install (Podman)
    ├── DOCKER_SCAN.md           # Docker scanning guide
    ├── DOCKER_TESTING.md        # Docker testing guide
    ├── DOCKER_TROUBLESHOOTING.md # Docker troubleshooting
    ├── GITHUB_UPLOAD.md         # GitHub upload guide
    └── QUICK_GITHUB_UPLOAD.md   # Quick GitHub upload
```

## Key Components

### CLI (`src/cli/`)
- **cli_main.py**: Main CLI entry point with commands (validate, scan, report, status, list, bot-scan, bot-audit, bot-deploy)
- **cli_tui.py**: Text User Interface for interactive mode
- **cli_validation.py**: Validation-specific commands

### Core (`src/core/`)
- **validator.py**: Validates ownership of files and systems
- **validation_engine.py**: Orchestrates validation processes

### Bot Security (`src/bots_security/`) *(NEW)*
- **models.py**: Data models — PlatformType, RiskLevel, FindingCategory, BotSecurityFinding, BotAuditResult
- **bot_scanner.py**: Scans bot source code for tokens, eval/exec, command injection, deserialization, rate limiting, webhook issues
- **webhook_guard.py**: Validates webhook HTTPS, secret verification, IP allowlist, payload size, timeouts
- **token_guard.py**: Detects leaked tokens for Telegram, Discord, Slack, VK; validates .env safety
- **audit_checklist.py**: Generates prioritized security checklists (HIGH/MEDIUM/LOW) + incident response plan
- **podman_templates.py**: Generates Containerfile, podman-compose.yml, nginx.conf, systemd unit, .env.example

### Safety (`src/safety/`)
- **safety_manager.py**: Manages safety levels (discovery, safe, moderate, aggressive)
- **models.py**: Safety data models
- **monitor.py**: Monitors system changes
- **progressive.py**: Progressive execution with rate limiting

### i18n (`src/i18n/`)
- **translation_manager.py**: Manages translations for multiple languages

### Knowledge Base (`src/knowledge_base/`)
- **knowledge_base.py**: Vulnerability patterns, fixes, and security rules

### AutoFix (`src/autofix/`)
- **autofix_engine.py**: Automatically fixes security issues

### Scanners (`src/scanners/`)
- **base_scanner.py**: Abstract base class for all scanners
- **scanner_factory.py**: Factory for creating scanners (supports lazy loading for bot scanner)
- **config_scanner.py**: Scans configuration files (YAML, JSON, XML, INI)
- **code_scanner.py**: Scans source code (Python, JS, TS, Java, C/C++, C#, Go, Ruby, PHP, Rust)
- **system_scanner.py**: Scans system security (Windows: updates, antivirus, firewall, users, ports, services)

### Tools (`src/tools/`)
- **base_tool.py**: Abstract base class for all tools
- **tool_factory.py**: Factory for creating tools
- **tool_manager.py**: Manages security tools

### Reporting (`src/reporting/`)
- **report_generator.py**: Generates security reports
- **formatters.py**: Report formatters (JSON, Text, HTML, Markdown)

### API (`src/api/`)
- **app.py**: FastAPI application factory with CORS

### Queue (`src/queue/`)
- **celery_app.py**: Celery task queue configuration

### Utilities (`src/utils/`)
- **config.py**: Settings class (pydantic-settings) + global `settings` instance
- **logger.py**: Logger factory + LoggerContext context manager
- **helpers.py**: Helper functions
- **exceptions.py**: Custom exceptions

## Safety Levels

1. **Discovery** - Read-only, no modifications
2. **Safe** - Non-destructive changes only
3. **Moderate** - Potentially destructive changes with warnings
4. **Aggressive** - All changes allowed

## Supported Languages

- English (en)
- Russian (ru)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (zh)
- Japanese (ja)
- Arabic (ar)
- Portuguese (pt)
- Italian (it)

## Installation

See `README.md` for installation instructions.

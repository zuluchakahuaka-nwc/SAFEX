# Changelog

All notable changes to SAFEX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-17

### Added
- Initial release of SAFEX (Security Audit Framework for Enhanced Protection)
- CLI with full command support (validate, scan, report, status, list)
- TUI (Text User Interface) for interactive usage
- 2-phase ownership validation system
- Safety levels: discovery, safe, moderate, aggressive
- Risk assessment with emoji warnings (🟢 LOW RISK, 🟡 MEDIUM RISK, 🔴 HIGH RISK, 🚨 CRITICAL)
- Internationalization (i18n) support for 10+ languages
  - English, Russian, Spanish, French, German, Chinese, Japanese, Arabic, Portuguese, Italian
- Knowledge base with 8 vulnerability patterns
- Security scanners:
  - Config Scanner (configuration files)
  - Code Scanner (source code)
  - System Scanner (system security)
- Report generation in multiple formats:
  - JSON, Text, HTML, Markdown, CSV
- Auto-fix engine with safety checks
- Backup management system
- System monitoring during scans
- Progressive execution with rate limiting
- Translation Manager with full Russian interface
- FastAPI REST API (ready for deployment)
- Podman support for containerized testing
- Systemd service for Ubuntu
- Comprehensive installation guides
- Comprehensive documentation:
  - README.md
  - SECURITY.md
  - SAFE_TESTING.md
  - README_I18N.md
  - PROJECT_STRUCTURE.md
  - Installation guides for Ubuntu

### Security
- 2-phase validation before any destructive actions
- Mandatory confirmations for high-risk operations
- Backup creation before modifications
- System health monitoring
- Rate limiting to prevent system overload

### Safety
- Discovery mode (read-only scanning)
- Safe mode (non-destructive changes only)
- Moderate mode (destructive changes with warnings)
- Aggressive mode (all changes allowed)

### i18n
- Full Russian interface
- Support for 10 languages
- CLI language selection (`--language ru`)
- TUI language support
- Web Console i18n support

### Documentation
- Comprehensive README with usage examples
- Security guidelines
- Safe testing practices
- Internationalization guide
- Project structure documentation
- Ubuntu installation guide

### Testing
- Basic tests (project structure, modules)
- Core module tests
- Safety module tests
- Config module tests

## [Unreleased]

### Added
- **Bot Security Module** (`src/bots_security/`) — security scanning and protection for messaging bot owners
  - BotScanner: scans bot source for token leaks, eval/exec, command injection, deserialization, rate limiting, webhook issues
  - WebhookGuard: validates HTTPS, secret verification, IP allowlist, payload size, timeouts
  - TokenGuard: detects leaked tokens for Telegram, Discord, Slack, VK; validates .env safety
  - AuditChecklist: generates prioritized security checklists (HIGH/MEDIUM/LOW) + incident response plan
  - PodmanTemplates: generates secure Containerfile, podman-compose.yml, nginx.conf, systemd unit, .env.example
  - Supports 7 platforms: Telegram, Discord, Slack, VK, Viber, WhatsApp, Generic
- Bot security knowledge base: 12 bot-specific vulnerabilities (BOT-001..BOT-012) and 12 security rules
- Podman deployment templates in `configs/podman/` (Containerfile, compose, nginx, systemd, .env)
- CLI commands: `bot-scan`, `bot-audit`, `bot-deploy`
- Scanner integration: `bot` scanner registered in ScannerFactory
- 31 tests for bot security module
- Architecture documentation (`docs/ARCHITECTURE.md`)
- AI Agent guide (`docs/AI_AGENT_GUIDE.md`)
- Updated PROJECT_STRUCTURE.md with bots_security module

### Planned
- More vulnerability patterns in knowledge base
- Additional scanners (network, vulnerability, web)
- Web Console UI
- Real-time monitoring dashboard
- CI/CD pipeline
- GitHub Actions
- More comprehensive test coverage
- Performance optimizations
- Additional language support

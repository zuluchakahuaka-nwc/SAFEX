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
- Docker support (alternative to pacman)
- Systemd service for Arch Linux / Manjaro
- PKGBUILD for easy installation via pacman
- Comprehensive documentation:
  - README.md
  - SECURITY.md
  - SAFE_TESTING.md
  - README_I18N.md
  - PROJECT_STRUCTURE.md
  - Installation guides for Arch Linux / Manjaro

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
- Arch Linux / Manjaro installation guide

### Testing
- Basic tests (project structure, modules)
- Core module tests
- Safety module tests
- Config module tests

## [Unreleased]

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

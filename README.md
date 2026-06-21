# SAFEX - Security Audit Framework for Enhanced Protection

**Comprehensive security scanning and validation framework with ownership verification and multi-language support**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-supported-orange.svg)](https://ubuntu.com/)
[![Podman](https://img.shields.io/badge/Podman-supported-blue.svg)](https://podman.io/)

---

## 📋 Table of Contents

- [Features](#features)
- [Safety Levels](#safety-levels)
  - [Installation](#installation)
   - [Ubuntu (Recommended)](#ubuntu-recommended)
   - [Other Linux Distributions](#other-linux-distributions)
  - [Windows](#windows)
  - [macOS](#macos)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Internationalization](#internationalization)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🔐 Ownership Validation
- 2-phase validation system
- Multiple validation methods (file permissions, registry, services, crypto)
- Automated batch validation

### 🔍 Security Scanning
- **Config Scanner** - Analyze configuration files for security issues
- **Code Scanner** - Detect vulnerabilities in source code
- **System Scanner** - Check system-level security
- **Vulnerability Scanner** - Scan for known vulnerabilities
- **Network Scanner** - Analyze network security
- **Web Scanner** - Test web applications
- **Bot Security Scanner** - Scan Telegram/Discord/Slack bots for vulnerabilities

### 🤖 Bot Security (NEW)
Specialized security module for messaging bot owners:
- **Token Leak Detection** - Finds exposed Telegram, Discord, Slack, VK tokens
- **Webhook Security** - Validates HTTPS, secret verification, IP allowlist, payload limits
- **Code Audit** - Detects eval/exec, command injection, deserialization, hardcoded secrets
- **Audit Checklist** - Generates prioritized security checklists (HIGH/MEDIUM/LOW)
- **Incident Response** - 7-step response plan for compromised bots
- **Podman Deployment** - Generates secure container templates (Containerfile, compose, nginx, systemd)
- Supports: Telegram, Discord, Slack, VK, Viber, WhatsApp

### 🛡️ Safety Levels
- **Discovery** - Read-only scanning
- **Safe** - Non-destructive changes only
- **Moderate** - Destructive changes with warnings
- **Aggressive** - All changes allowed

### 🌍 Internationalization (i18n)
Support for 10+ languages:
- 🇬🇧 English
- 🇷🇺 Русский
- 🇪🇸 Español
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇨🇳 中文
- 🇯🇵 日本語
- 🇸🇦 العربية
- 🇵🇹 Português
- 🇮🇹 Italiano

### 📊 Reporting
- Multiple report formats (JSON, Text, HTML, Markdown, CSV)
- Comprehensive vulnerability reports
- Fix recommendations
- Severity analysis with emoji indicators (🟢 LOW, 🟡 MEDIUM, 🔴 HIGH, 🚨 CRITICAL)

### 🔧 Auto-Fix
- Automatic vulnerability fixing
- Safety checks before modifications
- Backup creation before changes
- Rollback capability

### 🚀 System Integration
- Systemd service for Ubuntu
- Backup management
- System health monitoring
- Progressive execution with rate limiting

---

## ⚙️ Safety Levels

### Discovery Mode
- Read-only operations
- No system modifications
- Safe for production environments

### Safe Mode
- Non-destructive changes only
- Creates backups before modifications
- Requires confirmation for all changes

### Moderate Mode
- Potentially destructive changes
- Mandatory warnings
- Optional confirmations

### Aggressive Mode
- All changes allowed
- High-risk operations
- Not recommended for production

---

## 📦 Installation

### Ubuntu (Recommended)

#### Method 1: Using Podman Container (Recommended)

```bash
# Install Podman
sudo apt-get update
sudo apt-get install -y podman

# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Build and run Podman container
podman build -t safex .
podman run -it --rm -v $(pwd):/app safex
```

#### Method 2: Manual Installation

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv \
  python3-pyqt5 python3-requests python3-yaml python3-rich \
  python3-colorama python3-click python3-tqdm python3-psutil \
  python3-pygments python3-pytest python3-pyyaml \
  python3-cryptography nmap nikto sqlmap

# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run SAFEX
python safex.py --help
```

### Other Linux Distributions

```bash
# Install Python 3.9+
sudo apt-get install python3 python3-pip python3-venv  # Debian/Ubuntu
sudo yum install python3 python3-pip python3-venv     # Fedora/RHEL

# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run SAFEX
python safex.py --help
```

### Windows

```powershell
# Install Python 3.9+ from https://www.python.org/downloads/

# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run SAFEX
python safex.py --help
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run SAFEX
python safex.py --help
```

---

## 🚀 Quick Start

### Basic Usage

```bash
# Show help
safex --help

# Validate ownership of a target
safex validate /path/to/target

# Scan for security issues
safex scan /path/to/target

# Generate a report
safex report --format json

# Show system status
safex status

# List available scanners
safex list scanners
```

### With Russian Language

```bash
# Validate ownership
safex validate /path/to/target --language ru

# Scan for security issues
safex scan /path/to/target --language ru

# Generate report
safex report --format json --language ru
```

### Safety Level Examples

```bash
# Discovery mode (read-only)
safex scan /path/to/target --safety-level discovery

# Safe mode (non-destructive)
safex scan /path/to/target --safety-level safe

# Moderate mode (with warnings)
safex scan /path/to/target --safety-level moderate

# Aggressive mode (all changes)
safex scan /path/to/target --safety-level aggressive
```

---

## 📖 Usage

### CLI Commands

#### Validate Ownership

```bash
# Validate with auto-detection
safex validate /path/to/target

# Validate with specific method
safex validate /path/to/target --method file_permission

# Validate with safety level
safex validate /path/to/target --safety-level safe
```

#### Scan Target

```bash
# Scan with auto-detection
safex scan /path/to/target

# Scan with specific scanner
safex scan /path/to/target --scanner config

# Available scanners: config, code, system, vulnerability, network, web
```

#### Generate Report

```bash
# Generate JSON report
safex report --format json

# Generate HTML report
safex report --format html --output report.html

# Generate report with custom output
safex report --format markdown --output report.md
```

#### System Status

```bash
# Show system status
safex status

# List available scanners
safex list scanners

# List available tools
safex list tools

# List supported languages
safex list languages
```

#### Bot Security Commands

```bash
# Scan a bot project for vulnerabilities
safex bot-scan /path/to/bot-project --platform telegram

# Generate security audit checklist
safex bot-audit --platform telegram --text

# Generate JSON checklist
safex bot-audit --platform discord --output checklist.json

# Generate Podman deployment templates
safex bot-deploy --platform telegram --domain mybot.example.com --output-dir ./my-bot-deploy

# Scan with bot scanner (via unified scan command)
safex scan /path/to/bot-project --scanner bot
```

### Python API

```python
from src.core.validation_engine import ValidationEngine
from src.safety.safety_manager import SafetyManager
from src.i18n.translation_manager import TranslationManager

# Validate ownership
engine = ValidationEngine()
result = engine.validate_target("/path/to/target")

# Assess risk
sm = SafetyManager()
risk = sm.assess_fix_risk('VULN-001', '/path', 'CRITICAL')

# Get translations
tm = TranslationManager()
text = tm.translate('welcome', language='ru')
```

---

## 🌍 Internationalization

SAFEX supports 10+ languages:

| Language | Code | Status |
|----------|------|--------|
| English | `en` | ✅ Complete |
| Русский | `ru` | ✅ Complete |
| Español | `es` | ✅ Complete |
| Français | `fr` | ✅ Complete |
| Deutsch | `de` | ✅ Complete |
| 中文 | `zh` | ✅ Complete |
| 日本語 | `ja` | ✅ Complete |
| العربية | `ar` | ✅ Complete |
| Português | `pt` | ✅ Complete |
| Italiano | `it` | ✅ Complete |

### Changing Language

**CLI:**
```bash
safex validate /path --language ru
```

**Python API:**
```python
tm = TranslationManager()
text = tm.translate('welcome', language='ru')
```

### Adding New Language

1. Create language file in `src/i18n/translations/`
2. Add translations to the file
3. Register language in `TranslationManager`
4. Test translations

See [README_I18N.md](README_I18N.md) for detailed instructions.

---

## 📚 Documentation

- **[Main Documentation](README.md)** - This file
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Deep architecture, data flow, extension points
- **[AI Agent Guide](docs/AI_AGENT_GUIDE.md)** - Quick reference for AI coding agents
- **[Installation Guide for Ubuntu](docs/UBUNTU_INSTALL.md)** - Ubuntu installation with Podman
- **[Detailed Installation Guide](docs/INSTALLATION_UBUNTU.md)** - Comprehensive installation
- **[Security Guidelines](SECURITY.md)** - Security best practices
- **[Safe Testing Guide](SAFE_TESTING.md)** - Safe testing procedures
- **[Internationalization Guide](README_I18N.md)** - i18n documentation
- **[Project Structure](PROJECT_STRUCTURE.md)** - Project structure
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🧪 Testing

```bash
# Run all tests in Podman container
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ -v

# Run specific test file
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/test_basic.py -v

# Run with coverage
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ --cov=src --cov-report=html

# Run tests for specific module
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/test_core.py -v
```

---

## 🔧 Configuration

Configuration file location:
- **Ubuntu**: `/etc/safex/config.yaml`
- **Other Linux**: `~/.config/safex/config.yaml`
- **Windows**: `%APPDATA%\SAFEX\config.yaml`
- **macOS**: `~/Library/Application Support/SAFEX/config.yaml`

### Example Configuration

```yaml
safety:
  default_level: safe
  auto_backup: true
  backup_retention_days: 30

scanning:
  max_concurrent_scans: 1
  scan_timeout_minutes: 60

logging:
  level: INFO
  format: json
  file: /var/log/safex/safex.log

i18n:
  default_language: en
  auto_detect: true
```

---

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

For detailed contributing guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **GitHub Issues**: https://github.com/zuluchakahuaka-nwc/safex/issues
- **Documentation**: https://github.com/zuluchakahuaka-nwc/safex/wiki
- **Email**: support@safex.io (coming soon)

---

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with Python, FastAPI, and PyQt5
- Inspired by industry best practices in security auditing

---

## 📊 Project Stats

- **Version**: 1.0.0
- **Python Files**: 65+
- **Lines of Code**: 12,000+
- **Tests**: 47+
- **Languages Supported**: 10+
- **Vulnerabilities in KB**: 20+
- **Scanners**: 4+
- **Bot Platforms**: 7
- **Report Formats**: 5+

---

## 🔗 Links

- **GitHub**: https://github.com/zuluchakahuaka-nwc/safex
- **Documentation**: https://github.com/zuluchakahuaka-nwc/safex/wiki
- **PyPI**: https://pypi.org/project/safex/ (coming soon)

---

<div align="center">

**Made with ❤️ by the SAFEX Team**

[⬆ Back to Top](#safex---security-audit-framework-for-enhanced-protection)

</div>

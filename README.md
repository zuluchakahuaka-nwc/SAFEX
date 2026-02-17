# SAFEX - Security Audit Framework for Enhanced Protection

**Comprehensive security scanning and validation framework with ownership verification and multi-language support**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Arch Linux](https://img.shields.io/badge/Arch%20Linux-supported-blue.svg)](https://archlinux.org/)
[![Manjaro](https://img.shields.io/badge/Manjaro-supported-green.svg)](https://manjaro.org/)

---

## 📋 Table of Contents

- [Features](#features)
- [Safety Levels](#safety-levels)
- [Installation](#installation)
  - [Arch Linux / Manjaro (Recommended)](#arch-linux--manjaro-recommended)
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
- Systemd service for Arch Linux / Manjaro
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

### Arch Linux / Manjaro (Recommended)

#### Method 1: Using PKGBUILD

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Build and install
makepkg -si
```

#### Method 2: Using Installation Script

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Run installation script
sudo bash scripts/install_pacman.sh
```

#### Method 3: Manual Installation

```bash
# Install dependencies
sudo pacman -S python python-pip python-pyqt5 python-requests \
  python-yaml python-rich python-colorama python-click python-tqdm \
  python-psutil python-pygments python-pytest python-pyyaml \
  python-cryptography python-fastapi python-uvicorn python-redis \
  python-sqlalchemy nmap nikto sqlmap

# Clone and install
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
sudo bash scripts/install_pacman.sh
```

**For detailed installation instructions, see:**
- [Arch Linux / Manjaro Installation Guide](docs/ARCH_INSTALL.md)
- [Detailed Installation Guide](docs/INSTALLATION_ARCH.md)

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
- **[Installation Guide for Arch Linux](docs/ARCH_INSTALL.md)** - Arch/Manjaro installation
- **[Detailed Installation Guide](docs/INSTALLATION_ARCH.md)** - Comprehensive installation
- **[Security Guidelines](SECURITY.md)** - Security best practices
- **[Safe Testing Guide](SAFE_TESTING.md)** - Safe testing procedures
- **[Internationalization Guide](README_I18N.md)** - i18n documentation
- **[Project Structure](PROJECT_STRUCTURE.md)** - Project structure
- **[Changelog](CHANGELOG.md)** - Version history

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run tests for specific module
pytest tests/test_core.py -v
```

---

## 🔧 Configuration

Configuration file location:
- **Arch Linux / Manjaro**: `/etc/safex/config.yaml`
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
- **Python Files**: 57+
- **Lines of Code**: 10,000+
- **Tests**: 50+
- **Languages Supported**: 10+
- **Vulnerabilities in KB**: 8+
- **Scanners**: 6+
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

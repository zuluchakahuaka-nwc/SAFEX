# SAFEX Installation Guide for Arch Linux / Manjaro

## 📦 Installation Methods

### Method 1: Using PKGBUILD (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
```

2. **Build and install:**
```bash
makepkg -si
```

### Method 2: Using Installation Script

1. **Run the installation script:**
```bash
sudo bash scripts/install_pacman.sh
```

### Method 3: Manual Installation

1. **Install dependencies:**
```bash
sudo pacman -S python python-pip python-pyqt5 python-requests python-yaml \
  python-rich python-colorama python-click python-tqdm python-psutil \
  python-pygments python-pytest python-pyyaml python-cryptography \
  python-fastapi python-uvicorn python-redis python-sqlalchemy
```

2. **Clone and install:**
```bash
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
sudo bash scripts/install_pacman.sh
```

## 🗑️ Uninstallation

### Remove SAFEX:
```bash
sudo pacman -Rns safex
```

### Remove all data:
```bash
sudo pacman -Rns safex
sudo rm -rf /etc/safex /var/lib/safex /var/log/safex
```

## 📝 Configuration

Configuration file location: `/etc/safex/config.yaml`

Edit the configuration to customize SAFEX:
```bash
sudo nano /etc/safex/config.yaml
```

## 🚀 Usage

### Basic Commands:
```bash
# Show help
safex --help

# Validate ownership
safex validate <target>

# Scan for security issues
safex scan <target>

# Generate report
safex report --format json

# Show status
safex status

# List available scanners
safex list scanners
```

### With Russian Language:
```bash
safex validate <target> --language ru
safex scan <target> --language ru
```

### Safety Levels:
```bash
# Discovery mode (read-only)
safex scan <target> --safety-level discovery

# Safe mode (non-destructive)
safex scan <target> --safety-level safe

# Moderate mode (with warnings)
safex scan <target> --safety-level moderate

# Aggressive mode (all changes)
safex scan <target> --safety-level aggressive
```

## 🔧 Systemd Service

### Start service:
```bash
sudo systemctl start safex
```

### Stop service:
```bash
sudo systemctl stop safex
```

### Enable service (start on boot):
```bash
sudo systemctl enable safex
```

### Disable service:
```bash
sudo systemctl disable safex
```

### Check service status:
```bash
sudo systemctl status safex
```

### View logs:
```bash
sudo journalctl -u safex -f
```

## 📚 Documentation

Documentation location: `/usr/share/doc/safex/`

Available files:
- README.md - Main documentation
- SECURITY.md - Security guidelines
- SAFE_TESTING.md - Safe testing guidelines
- README_I18N.md - Internationalization
- PROJECT_STRUCTURE.md - Project structure

## 🌍 Supported Languages

- 🇬🇧 English (en)
- 🇷🇺 Русский (ru)
- 🇪🇸 Español (es)
- 🇫🇷 Français (fr)
- 🇩🇪 Deutsch (de)
- 🇨🇳 中文 (zh)
- 🇯🇵 日本語 (ja)
- 🇸🇦 العربية (ar)
- 🇵🇹 Português (pt)
- 🇮🇹 Italiano (it)

## 🛡️ Safety Levels

1. **Discovery** - Read-only scanning, no modifications
2. **Safe** - Non-destructive changes only
3. **Moderate** - Potentially destructive changes with warnings
4. **Aggressive** - All changes allowed

## 🔍 Available Scanners

- **config** - Configuration file scanner
- **code** - Source code scanner
- **system** - System security scanner
- **vulnerability** - Vulnerability scanner
- **network** - Network scanner
- **web** - Web application scanner

## 📊 Report Formats

- **json** - JSON format
- **text** - Plain text format
- **html** - HTML report
- **markdown** - Markdown format

## 🧪 Testing

Run tests:
```bash
cd /opt/safex
pytest tests/ -v
```

Run tests with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## 🆘 Troubleshooting

### Permission Issues:
```bash
sudo chmod +x /usr/bin/safex
sudo chmod -R 755 /opt/safex
```

### Import Errors:
```bash
cd /opt/safex
python -m pip install -r requirements.txt --upgrade
```

### Service Not Starting:
```bash
sudo journalctl -u safex -n 50
```

## 📞 Support

- GitHub: https://github.com/zuluchakahuaka-nwc/safex
- Issues: https://github.com/zuluchakahuaka-nwc/safex/issues

## 📄 License

MIT License - See LICENSE file for details

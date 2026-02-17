# SAFEX Arch Linux / Manjaro Installation

## Quick Install

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Run installation script
sudo bash scripts/install_pacman.sh
```

## Alternative: Build with PKGBUILD

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex

# Build package
makepkg -si
```

## Quick Start

```bash
# Show help
safex --help

# Validate ownership
safex validate /path/to/target

# Scan for security issues
safex scan /path/to/target --language ru

# Generate report
safex report --format json

# Show status
safex status
```

## Safety Levels

- `--safety-level discovery` - Read-only
- `--safety-level safe` - Non-destructive
- `--safety-level moderate` - With warnings
- `--safety-level aggressive` - All changes

## Languages

Use `--language` flag: `en`, `ru`, `es`, `fr`, `de`, `zh`, `ja`, `ar`, `pt`, `it`

Example:
```bash
safex scan /path --language ru
```

## Systemd Service

```bash
# Start service
sudo systemctl start safex

# Enable on boot
sudo systemctl enable safex

# View logs
sudo journalctl -u safex -f
```

## Uninstall

```bash
sudo pacman -Rns safex
sudo rm -rf /etc/safex /var/lib/safex /var/log/safex
```

## Support

📚 Documentation: `/usr/share/doc/safex/README.md`
🌐 GitHub: https://github.com/zuluchakahuaka-nwc/safex

# Detailed Installation Guide for SAFEX on Ubuntu

## Table of Contents

- [System Requirements](#system-requirements)
- [Pre-Installation Checks](#pre-installation-checks)
- [Installation Methods](#installation-methods)
  - [Method 1: Podman Container](#method-1-podman-container-recommended)
  - [Method 2: Manual Installation](#method-2-manual-installation)
- [Post-Installation Configuration](#post-installation-configuration)
- [Testing and Verification](#testing-and-verification)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)
- [Uninstallation](#uninstallation)

---

## System Requirements

### Minimum Requirements

- **OS**: Ubuntu 20.04 LTS / Debian 11+
- **CPU**: 2 cores (4 cores recommended)
- **RAM**: 4 GB (8 GB recommended)
- **Disk**: 2 GB free space (5 GB recommended)
- **Network**: Internet connection for package downloads

### Recommended Requirements

- **OS**: Ubuntu 22.04 LTS / Debian 12+
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Disk**: 10+ GB SSD
- **Network**: Stable internet connection

---

## Pre-Installation Checks

### Check Ubuntu Version

```bash
lsb_release -a
```

### Check Python Version

```bash
python3 --version
```

Expected output: `Python 3.9+`

### Check Available Memory

```bash
free -h
```

Make sure you have at least 4 GB available RAM.

### Check Disk Space

```bash
df -h
```

Make sure you have at least 2 GB free disk space.

---

## Installation Methods

### Method 1: Podman Container (Recommended)

#### Advantages of Podman

- **Isolation**: Runs in isolated container
- **Consistency**: Same environment across all systems
- **Security**: Additional security layer
- **Portability**: Easy to deploy

#### Step 1: Install Podman

```bash
# Update package list
sudo apt-get update

# Install Podman
sudo apt-get install -y podman

# Verify installation
podman --version

# Check Podman status
podman info
```

#### Step 2: Configure Podman User Namespace (Optional)

For better security, enable user namespaces:

```bash
# Enable user namespaces
echo "$USER:100000:65536" | sudo tee -a /etc/subuid
echo "$USER:100000:65536" | sudo tee -a /etc/subgid

# Restart Podman service
sudo systemctl restart podman
```

#### Step 3: Clone SAFEX Repository

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git

# Navigate to directory
cd safex

# Verify contents
ls -la
```

#### Step 4: Build Podman Image

```bash
# Build the image
podman build -t safex:latest .

# Verify the image
podman images | grep safex

# Expected output:
# safex    latest    abc123def456    2 minutes ago    1.2 GB
```

#### Step 5: Run SAFEX in Podman

```bash
# Basic usage
podman run -it --rm safex:latest

# With volume mount (for persistence)
podman run -it --rm -v $(pwd)/data:/app/data safex:latest

# Run specific command
podman run --rm safex:latest python safex.py --help

# Run scan
podman run --rm safex:latest python safex.py scan /path/to/target
```

#### Step 6: Create Alias (Optional)

```bash
# Add alias to ~/.bashrc
echo "alias safex='podman run --rm -v \$(pwd):/app safex:latest python safex.py'" >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Use alias
safex --help
```

### Method 2: Manual Installation

#### Step 1: Install System Dependencies

```bash
# Update package list
sudo apt-get update

# Install Python and essential dependencies
sudo apt-get install -y python3 python3-pip python3-venv python3-dev \
  build-essential libssl-dev libffi-dev

# Install PyQt5 (for GUI)
sudo apt-get install -y python3-pyqt5

# Install network tools
sudo apt-get install -y nmap nikto sqlmap

# Install additional Python packages
sudo apt-get install -y python3-requests python3-yaml python3-rich \
  python3-colorama python3-click python3-tqdm python3-psutil \
  python3-pygments python3-pytest python3-pyyaml python3-cryptography
```

#### Step 2: Clone SAFEX Repository

```bash
# Clone repository
git clone https://github.com/zuluchakahuaka-nwc/safex.git

# Navigate to directory
cd safex
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Verify creation
ls -la venv/

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) in prompt)
which python
```

#### Step 4: Upgrade PIP and Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

#### Step 5: Run SAFEX

```bash
# Show help
python safex.py --help

# Show version
python safex.py --version

# Run basic scan
python safex.py scan /path/to/target
```

---

## Post-Installation Configuration

### Create Configuration File

```bash
# Create config directory
sudo mkdir -p /etc/safex

# Create default config
sudo nano /etc/safex/config.yaml
```

Add the following configuration:

```yaml
# SAFEX Configuration
safety:
  default_level: safe
  auto_backup: true
  backup_retention_days: 30
  backup_location: /var/lib/safex/backups

scanning:
  max_concurrent_scans: 1
  scan_timeout_minutes: 60
  exclude_patterns:
    - "*.log"
    - "*.tmp"
    - "node_modules/*"

logging:
  level: INFO
  format: json
  file: /var/log/safex/safex.log
  max_size_mb: 100
  backup_count: 5

i18n:
  default_language: en
  auto_detect: true

api:
  enabled: false
  host: 0.0.0.0
  port: 8000
  debug: false
```

### Create Log Directory

```bash
# Create log directory
sudo mkdir -p /var/log/safex

# Set permissions
sudo chown -R $USER:$USER /var/log/safex

# Create log file
touch /var/log/safex/safex.log
```

### Create Backup Directory

```bash
# Create backup directory
sudo mkdir -p /var/lib/safex/backups

# Set permissions
sudo chown -R $USER:$USER /var/lib/safex
```

---

## Testing and Verification

### Basic Functionality Tests

```bash
# Test basic scan
python safex.py scan /tmp

# Test with specific scanner
python safex.py scan /tmp --scanner config

# Test report generation
python safex.py report --format json
```

### Run Test Suite

#### Using Podman

```bash
# Run all tests
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ -v

# Run with coverage
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ --cov=src --cov-report=html

# Run specific test
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/test_basic.py -v
```

#### Manual Installation

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
firefox htmlcov/index.html
```

### Verify Installation

```bash
# Check SAFEX version
python safex.py --version

# Check available scanners
python safex.py list scanners

# Check system status
python safex.py status
```

---

## Troubleshooting

### Podman Issues

#### Podman not found

```bash
# Install Podman
sudo apt-get install -y podman

# Verify installation
podman --version
```

#### Permission denied

```bash
# Add user to podman group
sudo usermod -aG podman $USER

# Logout and login again
# Or run:
newgrp podman
```

#### Container won't start

```bash
# Check Podman status
sudo systemctl status podman

# Check logs
sudo journalctl -xeu podman

# Restart Podman
sudo systemctl restart podman
```

### Python/PIP Issues

#### Module not found

```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

#### PIP upgrade failed

```bash
# Upgrade pip using system pip
python3 -m pip install --upgrade pip

# Reinstall virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Issues

#### Cannot write to /var/log/safex

```bash
# Fix permissions
sudo chown -R $USER:$USER /var/log/safex

# Or run with sudo (not recommended)
sudo python safex.py scan /path/to/target
```

#### Cannot write to /etc/safex

```bash
# Fix permissions
sudo chown -R $USER:$USER /etc/safex

# Or run with sudo
sudo nano /etc/safex/config.yaml
```

---

## Advanced Configuration

### Systemd Service

Create systemd service file for automatic startup:

```bash
sudo nano /etc/systemd/system/safex.service
```

Add the following content:

```ini
[Unit]
Description=SAFEX Security Scanner
After=network.target

[Service]
Type=simple
User=safex
Group=safex
WorkingDirectory=/opt/safex
Environment="PATH=/opt/safex/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/safex/venv/bin/python /opt/safex/safex.py daemon
Restart=on-failure
RestartSec=10
StandardOutput=append:/var/log/safex/safex.log
StandardError=append:/var/log/safex/safex.log

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
# Create safex user
sudo useradd -r -s /bin/false safex

# Create directories
sudo mkdir -p /opt/safex
sudo mkdir -p /var/lib/safex
sudo mkdir -p /var/log/safex

# Set permissions
sudo chown -R safex:safex /opt/safex
sudo chown -R safex:safex /var/lib/safex
sudo chown -R safex:safex /var/log/safex

# Copy SAFEX files
sudo cp -r /path/to/safex/* /opt/safex/

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable safex
sudo systemctl start safex

# Check status
sudo systemctl status safex
```

### Cron Jobs

For periodic scanning:

```bash
# Open crontab
crontab -e

# Add daily scan (runs at 2 AM)
0 2 * * * /opt/safex/venv/bin/python /opt/safex/safex.py scan /path/to/target --report-format json --report-output /tmp/scan_report.json

# Add weekly report (runs on Sunday at 3 AM)
0 3 * * 0 /opt/safex/venv/bin/python /opt/safex/safex.py report --format html --report-output /tmp/weekly_report.html
```

---

## Uninstallation

### Podman Installation

```bash
# Remove Podman images
podman rmi safex:latest

# Remove source code
cd ..
rm -rf safex

# Remove Podman (optional)
sudo apt-get remove podman

# Remove user namespace configs (if configured)
sudo sed -i "/$USER:100000:65536/d" /etc/subuid
sudo sed -i "/$USER:100000:65536/d" /etc/subgid
```

### Manual Installation

```bash
# Deactivate virtual environment
deactivate

# Remove source code
cd ..
rm -rf safex

# Remove Python packages (optional)
pip uninstall -y safex

# Remove configuration (optional)
sudo rm -rf /etc/safex
sudo rm -rf /var/log/safex
sudo rm -rf /var/lib/safex

# Remove systemd service (if installed)
sudo systemctl disable safex
sudo systemctl stop safex
sudo rm /etc/systemd/system/safex.service
sudo systemctl daemon-reload
```

---

## Support and Resources

- **GitHub Repository**: https://github.com/zuluchakahuaka-nwc/safex
- **Issues**: https://github.com/zuluchakahuaka-nwc/safex/issues
- **Documentation**: https://github.com/zuluchakahuaka-nwc/safex/wiki
- **Podman Documentation**: https://podman.io/docs/

---

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

# Ubuntu Installation Guide for SAFEX

## Prerequisites

- Ubuntu 20.04+ / Debian 11+
- Python 3.9+
- Podman 3.0+

## Installation Methods

### Method 1: Using Podman Container (Recommended)

This is the recommended method as it provides a consistent, isolated environment.

#### Step 1: Install Podman

```bash
# Update package list
sudo apt-get update

# Install Podman
sudo apt-get install -y podman

# Verify installation
podman --version
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
```

#### Step 3: Build Podman Image

```bash
# Build the image
podman build -t safex .

# Verify the image
podman images | grep safex
```

#### Step 4: Run SAFEX in Podman

```bash
# Run interactive session
podman run -it --rm -v $(pwd):/app safex

# Run specific command
podman run --rm -v $(pwd):/app safex python safex.py --help

# Run scan
podman run --rm -v $(pwd):/app safex python safex.py scan /path/to/target
```

### Method 2: Manual Installation

#### Step 1: Install System Dependencies

```bash
# Update package list
sudo apt-get update

# Install Python and dependencies
sudo apt-get install -y python3 python3-pip python3-venv \
  python3-pyqt5 python3-requests python3-yaml python3-rich \
  python3-colorama python3-click python3-tqdm python3-psutil \
  python3-pygments python3-pytest python3-pyyaml \
  python3-cryptography nmap nikto sqlmap
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### Step 4: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt
```

#### Step 5: Run SAFEX

```bash
# Show help
python safex.py --help

# Run scan
python safex.py scan /path/to/target
```

## Running Tests

### Using Podman

```bash
# Run all tests
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ -v

# Run with coverage
podman run --rm -v "$(pwd):/app" -w /app python:3.11 pytest tests/ --cov=src --cov-report=html
```

### Manual Installation

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Systemd Service (Optional)

### For Podman

Create a systemd service file:

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
ExecStart=/usr/bin/podman run --rm -v /opt/safex:/app safex
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Create safex user
sudo useradd -r -s /bin/false safex

# Create directory
sudo mkdir -p /opt/safex
sudo chown -R safex:safex /opt/safex

# Enable and start service
sudo systemctl enable safex
sudo systemctl start safex

# Check status
sudo systemctl status safex
```

## Configuration

Configuration file location:
- **Ubuntu**: `/etc/safex/config.yaml`

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

## Uninstallation

### Podman Installation

```bash
# Remove images
podman rmi safex

# Remove source
cd ..
rm -rf safex

# Remove Podman (optional)
sudo apt-get remove podman
```

### Manual Installation

```bash
# Deactivate virtual environment
deactivate

# Remove source
cd ..
rm -rf safex

# Remove Python dependencies (optional)
sudo apt-get remove python3-safex
```

## Troubleshooting

### Podman Permission Issues

If you encounter permission issues with Podman:

```bash
# Add user to podman group
sudo usermod -aG podman $USER

# Logout and login again
```

### Virtual Environment Issues

```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### System Requirements

Make sure you have enough system resources:

```bash
# Check available memory
free -h

# Check disk space
df -h

# Check CPU
lscpu
```

## Support

For issues and support:
- **GitHub Issues**: https://github.com/zuluchakahuaka-nwc/safex/issues
- **Documentation**: https://github.com/zuluchakahuaka-nwc/safex/wiki

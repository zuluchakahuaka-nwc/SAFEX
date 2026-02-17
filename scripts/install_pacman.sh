#!/bin/bash

# SAFEX Installation Script for Arch Linux / Manjaro
# This script installs SAFEX using pacman

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           SAFEX - Security Audit Framework                ║"
    echo "║                                                          ║"
    echo "║              Installation Script (pacman)                  ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root"
        print_info "Use: sudo $0"
        exit 1
    fi
}

# Check if pacman is available
check_pacman() {
    if ! command -v pacman &> /dev/null; then
        print_error "pacman is not installed or not in PATH"
        exit 1
    fi
}

# Update system
update_system() {
    print_info "Updating system packages..."
    pacman -Syu --noconfirm || true
    print_success "System updated"
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    # Core Python packages
    pacman -S --noconfirm --needed \
        python \
        python-pip \
        python-setuptools \
        python-wheel \
        python-virtualenv \
        python-pyqt5 \
        python-pyqt5-sip \
        python-pyqtwebengine \
        python-requests \
        python-yaml \
        python-rich \
        python-colorama \
        python-click \
        python-tqdm \
        python-psutil \
        python-pygments \
        python-pylint \
        python-pytest \
        python-pytest-cov \
        python-coverage \
        python-pytest-mock \
        python-mock \
        python-pydocstyle \
        python-black \
        python-isort \
        python-flake8 \
        python-mypy \
        python-bandit \
        python-safety \
        python-pytest \
        python-pyyaml \
        python-cryptography \
        python-pyopenssl \
        python-certifi \
        python-fastapi \
        python-uvicorn \
        python-gunicorn \
        python-redis \
        python-hiredis \
        python-sqlalchemy \
        python-psycopg2 \
        python-pymysql \
        python-alembic \
        python-marshmallow \
        python-prometheus-client \
        python-prometheus-fastapi-instrumentator \
        python-loguru \
        python-colorlog \
        python-structlog \
        python-json-logging \
        python-babel \
        python-chardet \
        python-idna \
        python-h11 \
        python-h2 \
        python-hpack \
        python-hyperframe \
        python-priority \
        python-pyasn1 \
        python-pyasn1-modules \
        python-cffi \
        python-pycparser \
        python-ruamel-yaml \
        python-toml \
        python-tomli \
        python-tomli-w \
        python-click-default-group \
        python-click-completion \
        python-click-log \
        python-sentry-sdk \
        python-aiomysql \
        python-asyncpg \
        python-aiosqlite \
        python-pytest-asyncio \
        python-pytest-benchmark \
        python-pytest-html \
        python-pytest-xdist \
        python-pytest-timeout \
        python-pytest-ordering \
        python-faker \
        python-freezegun \
        python-responses \
        python-pyfakefs \
        python-pkginfo \
        python-readme-renderer \
        python-packaging \
        python-pyparsing \
        python-pytz \
        python-service-identity \
        python-urllib3 \
        python-charset-normalizer \
        python-websockets \
        python-uvloop \
        python-httptools \
        python-priority \
        python-vine \
        python-amqp \
        python-pika \
        python-billiard \
        python-kombu \
        python-annotated-types \
        python-typing-extensions \
        python-pydantic \
        python-pydantic-core \
        python-pydantic-settings \
        python-jsonschema \
        python-jsonlines \
        python-six \
        python-ecs-logging || true

    print_success "Python dependencies installed"
}

# Install optional tools
install_optional_tools() {
    print_info "Installing optional security tools..."

    pacman -S --noconfirm --needed \
        nmap \
        nikto \
        sqlmap \
        netcat \
        tcpdump \
        wireshark-cli || true

    print_success "Optional tools installed"
}

# Create directories
create_directories() {
    print_info "Creating directories..."

    mkdir -p /opt/safex
    mkdir -p /etc/safex
    mkdir -p /var/lib/safex/knowledge_base
    mkdir -p /var/log/safex
    mkdir -p /var/lib/safex/backups
    mkdir -p /usr/share/licenses/safex
    mkdir -p /usr/share/doc/safex

    # Set permissions
    chmod 755 /opt/safex
    chmod 755 /etc/safex
    chmod 755 /var/lib/safex
    chmod 755 /var/lib/safex/knowledge_base
    chmod 755 /var/log/safex
    chmod 755 /var/lib/safex/backups
    chmod 755 /usr/share/licenses/safex
    chmod 755 /usr/share/doc/safex

    print_success "Directories created"
}

# Install SAFEX files
install_safex_files() {
    print_info "Installing SAFEX files..."

    # Copy source files
    cp -r src/* /opt/safex/src/

    # Copy configs
    cp -r configs/* /etc/safex/

    # Copy knowledge base
    cp -r knowledge_base/* /var/lib/safex/knowledge_base/

    # Copy scripts
    cp -r scripts/* /opt/safex/scripts/

    # Copy main executable
    cp safex.py /opt/safex/safex.py
    chmod +x /opt/safex/safex.py

    # Create symlink in /usr/bin
    ln -sf /opt/safex/safex.py /usr/bin/safex
    chmod +x /usr/bin/safex

    # Copy documentation
    cp README.md /usr/share/doc/safex/ 2>/dev/null || true
    cp SECURITY.md /usr/share/doc/safex/ 2>/dev/null || true
    cp SAFE_TESTING.md /usr/share/doc/safex/ 2>/dev/null || true
    cp README_I18N.md /usr/share/doc/safex/ 2>/dev/null || true
    cp PROJECT_STRUCTURE.md /usr/share/doc/safex/ 2>/dev/null || true
    cp LICENSE /usr/share/licenses/safex/ 2>/dev/null || true

    print_success "SAFEX files installed"
}

# Install Python requirements via pip
install_pip_requirements() {
    print_info "Installing Python requirements via pip..."

    cd /opt/safex
    python -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt --upgrade || true

    print_success "Python requirements installed"
}

# Create systemd service (optional)
create_systemd_service() {
    print_info "Creating systemd service..."

    cat > /usr/lib/systemd/system/safex.service << 'EOF'
[Unit]
Description=SAFEX Security Audit Framework
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/safex
ExecStart=/usr/bin/safex status
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable safex.service

    print_success "Systemd service created"
}

# Print completion message
print_completion() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           SAFEX installed successfully!                    ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 Installation Location: /opt/safex"
    echo "🔧 Configuration: /etc/safex"
    echo "📚 Knowledge Base: /var/lib/safex/knowledge_base"
    echo "📝 Logs: /var/log/safex"
    echo ""
    echo "🚀 Quick Start:"
    echo "   $ safex --help"
    echo "   $ safex validate <target>"
    echo "   $ safex scan <target> --language ru"
    echo ""
    echo "🌍 Supported Languages: en, ru, es, fr, de, zh, ja, ar, pt, it"
    echo ""
    echo "⚙️  Configuration:"
    echo "   Edit /etc/safex/config.yaml to customize SAFEX"
    echo ""
    echo "📖 Documentation:"
    echo "   /usr/share/doc/safex/README.md"
    echo "   https://github.com/zuluchakahuaka-nwc/safex"
    echo ""
    echo "🛡️  Safety Levels:"
    echo "   - discovery: Read-only scanning"
    echo "   - safe: Non-destructive changes"
    echo "   - moderate: Destructive changes with warnings"
    echo "   - aggressive: All changes allowed"
    echo ""
    echo "🔧 Systemd Service:"
    echo "   $ sudo systemctl start safex"
    echo "   $ sudo systemctl stop safex"
    echo "   $ sudo systemctl enable safex"
    echo "   $ sudo systemctl disable safex"
    echo ""
    echo "✅ Installation complete!"
    echo ""
}

# Main installation
main() {
    print_header

    print_info "Starting SAFEX installation..."
    echo ""

    check_root
    check_pacman
    update_system
    install_python_deps
    install_optional_tools
    create_directories
    install_safex_files
    install_pip_requirements
    create_systemd_service

    print_completion
}

# Run main function
main

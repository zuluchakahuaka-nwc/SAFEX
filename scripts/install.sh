#!/bin/bash

# SAFEX Installation Script
# This script installs and configures SAFEX

set -e

echo "================================"
echo "SAFEX Installation Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!] ${NC} $1"
}

print_error() {
    echo -e "${RED}[X]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root is not recommended"
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    print_success "Detected Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_success "Detected macOS"
else
    print_error "Unsupported OS: $OSTYPE"
    exit 1
fi

# Check Python
echo ""
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION installed"
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Check pip
echo ""
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 installed"
else
    print_error "pip3 not found. Please install pip"
    exit 1
fi

# Install system dependencies
echo ""
echo "Installing system dependencies..."

if [ "$OS" == "linux" ]; then
    # Debian/Ubuntu
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y \
            nmap \
            nikto \
            python3-dev \
            build-essential \
            libssl-dev \
            libffi-dev \
            curl \
            git \
            && rm -rf /var/lib/apt/lists/*
        print_success "System dependencies installed (apt-get)"
    elif command -v yum &> /dev/null; then
        # RHEL/CentOS
        sudo yum install -y \
            nmap \
            nikto \
            python3-devel \
            gcc \
            openssl-devel \
            git
        print_success "System dependencies installed (yum)"
    else
        print_warning "Could not detect package manager. Please install nmap and nikto manually"
    fi
elif [ "$OS" == "macos" ]; then
    if command -v brew &> /dev/null; then
        brew install nmap nikto
        print_success "System dependencies installed (brew)"
    else
    print_warning "Homebrew not found. Please install nmap and nikto manually"
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    pip install --upgrade pip setuptools wheel pyinstaller
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Setup environment
echo ""
echo "Setting up environment..."

if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from .env.example"
        print_warning "Please edit .env file with your configuration"
    else
        print_error ".env.example not found"
        exit 1
fi

# Create directories
echo ""
echo "Creating directories..."

mkdir -p data/backups
mkdir -p data/temp
mkdir -p data/wordlists
mkdir -p data/exploits
mkdir -p reports
mkdir -p logs
print_success "Directories created"

# Setup database (optional)
echo ""
echo "Database setup..."
print_warning "Database setup requires PostgreSQL. Please configure DATABASE_URL in .env file"

# Install OpenVAS (optional)
echo ""
echo "OpenVAS installation..."
print_warning "OpenVAS installation is optional. Please install manually if needed."

# Install OWASP ZAP (optional)
echo ""
echo "OWASP ZAP installation..."
print_warning "OWASP ZAP installation is optional. Please install manually if needed."

# Final check
echo ""
echo "================================"
echo "Installation Complete!"
echo "================================"
echo ""

echo "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Configure DATABASE_URL"
echo "  3. Install OpenVAS (optional): see above"
echo "  4. Install OWASP ZAP (optional): see above"
echo " 5. Run: safex --help"
echo "echo ""
echo "Commands:"
echo "  - Activate environment: source venv/bin/activate"
echo "  - Run CLI: safex --help"
echo "  - Validate: safex validate --domain example.com --target-email admin@example.com"
echo "  - Start scan: safex scan --target 1.2.3.4 --token <token>"
echo "  - Generate report: safex report --scan-id <uuid> --format json,html,pdf"
echo "echo ""
echo "For deployment:"
echo "  - Local: docker-compose up -d"
echo "  - Cloud: docker-compose -f docker-compose.yml up -d"
echo ""
echo "Happy testing!"

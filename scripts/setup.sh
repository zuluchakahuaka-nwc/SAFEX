#!/bin/bash

# SAFEX Setup Script
# This script configures and runs SAFEX

set -e

echo "================================"
echo "SAFEX Setup Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to confirm action
confirm_action() {
    echo ""
    read -p "Continue? [y/N]: " answer
    if [ "$answer" != "y" ]; then
        echo ""
        echo "Cancelled."
        exit 1
    fi
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

# Check dependencies
echo ""
echo "Checking dependencies..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION available"
else
    print_error "Python 3.11+ required but not found"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_success "pip3 available"
else
    print_error "pip3 required but not found"
    exit 1
fi

# Check system dependencies
echo ""
echo "Checking system dependencies..."

# Nmap
if command -v nmap &> /dev/null; then
    NMAP_VERSION=$(nmap --version | grep -oP "^Nmap version [0-9.]+.[0-9]+.")
    print_success "Nmap $NMAP_VERSION available"
else
    print_warning "Nmap not found. Please install: https://nmap.org/download/"
fi

# Nikto
if command -v nikto &> /dev/null; then
    print_success "Nikto available"
else
    print_warning "Nikto not found. Please install: https://github.com/sullo/nikto"
fi

# Git
if command -v git &> /dev/null; then
    print_success "Git available"
else
    print_warning "Git not found. Please install: https://git-scm.com/"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
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
        print_success ".env created from .env.example"
        print_warning "Please edit .env file with your configuration"
    else
        print_warning ".env.example not found"
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

# Database setup
echo ""
echo "Database setup:"
echo "  1. Install PostgreSQL: https://www.postgresql.org/download/"
echo "  2. Create database: createdb safex_db"
echo "  3. Create user: create user safex with password safex_password"
echo "  4. Grant privileges: GRANT ALL PRIVILEGES ON DATABASE safex_db TO safex;"
echo "   5. Configure DATABASE_URL in .env file"

echo ""
echo "Configuration complete!"
echo ""

# Final message
echo ""
echo "================================"
echo "SAFEX Setup Complete!"
echo "================================"
echo ""
echo ""
echo "Quick start:"
echo ""
echo "  source venv/bin/activate"
echo "  safex --help"
echo ""
echo "For local deployment:"
echo "  docker-compose up -d"
echo ""
echo "Happy security testing!"

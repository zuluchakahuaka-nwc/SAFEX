# SAFEX Project Structure

This document describes the complete structure of the SAFEX project.

## Directory Structure

```
SAFEX/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables example
├── SECURITY.md                  # Security guidelines
├── SAFE_TESTING.md             # Safe testing guidelines
├── README_I18N.md              # Internationalization documentation
├── safex.py                    # CLI entry point
├── src/                        # Source code
│   ├── __init__.py
│   ├── cli/                    # Command-line interface
│   │   ├── __init__.py
│   │   ├── cli_main.py         # Main CLI implementation
│   │   ├── cli_tui.py          # Text User Interface
│   │   └── cli_validation.py   # Validation commands
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py         # Settings class
│   │   └── config_loader.py    # Configuration loader
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── validator.py        # Ownership validator
│   │   └── validation_engine.py # Validation engine
│   ├── safety/                 # Safety features
│   │   ├── __init__.py
│   │   ├── safety_manager.py   # Safety level manager
│   │   ├── backup.py           # Backup manager
│   │   ├── monitor.py          # Monitoring system
│   │   └── progressive.py       # Progressive execution
│   ├── i18n/                   # Internationalization
│   │   ├── __init__.py
│   │   └── translation_manager.py # Translation manager
│   ├── knowledge_base/         # Vulnerability knowledge base
│   │   ├── __init__.py
│   │   └── knowledge_base.py   # Knowledge base manager
│   ├── autofix/                # Auto-fix functionality
│   │   ├── __init__.py
│   │   └── autofix_engine.py   # Auto-fix engine
│   ├── scanners/               # Security scanners
│   │   ├── __init__.py
│   │   ├── base_scanner.py     # Base scanner class
│   │   ├── scanner_factory.py  # Scanner factory
│   │   ├── config_scanner.py   # Configuration scanner
│   │   ├── code_scanner.py     # Source code scanner
│   │   └── system_scanner.py   # System scanner
│   ├── tools/                  # Security tools
│   │   ├── __init__.py
│   │   ├── base_tool.py        # Base tool class
│   │   ├── tool_factory.py     # Tool factory
│   │   └── tool_manager.py     # Tool manager
│   ├── reporting/              # Reporting system
│   │   ├── __init__.py
│   │   ├── report_generator.py # Report generator
│   │   └── formatters.py       # Report formatters
│   ├── api/                    # API (future)
│   │   ├── __init__.py
│   │   ├── app.py             # FastAPI application
│   │   ├── routes/            # API routes
│   │   └── middleware/        # API middleware
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── logger.py          # Logger utility
├── tests/                      # Tests
│   ├── __init__.py
│   ├── test_basic.py          # Basic tests
│   ├── test_core.py           # Core module tests
│   ├── test_safety.py         # Safety module tests
│   └── test_config.py         # Config module tests
├── configs/                    # Configuration files
│   ├── safety_config.yaml     # Safety levels config
│   ├── scan_profiles.yaml     # Scan profiles
│   └── tools_config.yaml      # Tools configuration
├── knowledge_base/             # Knowledge base data
│   ├── vulnerabilities.json    # Vulnerability database
│   ├── fix_recommendations.json # Fix recommendations
│   └── security_rules.yaml    # Security rules
├── scripts/                    # Installation and setup scripts
│   ├── install.sh             # Linux/macOS install
│   ├── setup.sh               # Linux/macOS setup
│   └── setup.bat              # Windows setup
├── docker/                     # Docker configuration
│   ├── docker-compose.yml     # Docker Compose
│   └── Dockerfile             # Docker image
└── frontend/                   # Frontend (React)
    ├── package.json
    ├── tsconfig.json
    └── src/
        └── ...

```

## Key Components

### CLI (`src/cli/`)
- **cli_main.py**: Main CLI entry point with commands
- **cli_tui.py**: Text User Interface for interactive mode
- **cli_validation.py**: Validation-specific commands

### Core (`src/core/`)
- **validator.py**: Validates ownership of files and systems
- **validation_engine.py**: Orchestrates validation processes

### Safety (`src/safety/`)
- **safety_manager.py**: Manages safety levels (discovery, safe, moderate, aggressive)
- **backup.py**: Creates and manages backups
- **monitor.py**: Monitors system changes
- **progressive.py**: Progressive execution with rate limiting

### i18n (`src/i18n/`)
- **translation_manager.py**: Manages translations for multiple languages

### Knowledge Base (`src/knowledge_base/`)
- **knowledge_base.py**: Vulnerability patterns, fixes, and security rules

### AutoFix (`src/autofix/`)
- **autofix_engine.py**: Automatically fixes security issues

### Scanners (`src/scanners/`)
- **base_scanner.py**: Abstract base class for all scanners
- **scanner_factory.py**: Factory for creating scanners
- **config_scanner.py**: Scans configuration files
- **code_scanner.py**: Scans source code
- **system_scanner.py**: Scans system security

### Tools (`src/tools/`)
- **base_tool.py**: Abstract base class for all tools
- **tool_factory.py**: Factory for creating tools
- **tool_manager.py**: Manages security tools

### Reporting (`src/reporting/`)
- **report_generator.py**: Generates security reports
- **formatters.py**: Report formatters (JSON, Text, HTML, Markdown)

## Safety Levels

1. **Discovery** - Read-only, no modifications
2. **Safe** - Non-destructive changes only
3. **Moderate** - Potentially destructive changes with warnings
4. **Aggressive** - All changes allowed

## Supported Languages

- English (en)
- Russian (ru)
- Spanish (es)
- French (fr)
- German (de)
- Chinese (zh)
- Japanese (ja)
- Arabic (ar)
- Portuguese (pt)
- Italian (it)

## Installation

See `README.md` for installation instructions.

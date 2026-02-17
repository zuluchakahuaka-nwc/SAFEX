# Maintainer: Your Name <your@email.com>
# Contributor: SAFEX Team <safex@example.com>

pkgname=safex
pkgver=1.0.0
pkgrel=1
pkgdesc="Security Audit Framework for Enhanced Protection - Comprehensive security scanning and validation tool"
arch=('any')
url="https://github.com/zuluchakahuaka-nwc/safex"
license=('MIT')
depends=(
    'python>=3.9'
    'python-pyqt5'
    'python-pyqt5-sip'
    'python-pyqtwebengine'
    'python-requests'
    'python-yaml'
    'python-rich'
    'python-colorama'
    'python-click'
    'python-tqdm'
    'python-psutil'
    'python-pygments'
    'python-pylint'
    'python-pytest'
    'python-pytest-cov'
    'python-coverage'
    'python-pytest-mock'
    'python-mock'
    'python-pydocstyle'
    'python-black'
    'python-isort'
    'python-flake8'
    'python-mypy'
    'python-bandit'
    'python-safety'
    'python-auditwheel'
    'python-setuptools'
    'python-wheel'
    'python-pip'
    'python-virtualenv'
    'python-pipenv'
    'python-poetry'
    'python-build'
    'python-twine'
    'python-pkginfo'
    'python-readme-renderer'
    'python-pygments'
    'python-six'
    'python-typing-extensions'
    'python-pydantic'
    'python-pydantic-settings'
    'python-pydantic-core'
    'python-annotated-types'
    'python-pyyaml'
    'python-jsonschema'
    'python-jsonlines'
    'python-tomli'
    'python-tomli-w'
    'python-packaging'
    'python-pyparsing'
    'python-pytz'
    'python-babel'
    'python-chardet'
    'python-idna'
    'python-cryptography'
    'python-openssl'
    'python-service-identity'
    'python-pyopenssl'
    'python-certifi'
    'python-urllib3'
    'python-charset-normalizer'
    'python-h11'
    'python-h2'
    'python-hpack'
    'python-hyperframe'
    'python-priority'
    'python-pyasn1'
    'python-pyasn1-modules'
    'python-idna'
    'python-cffi'
    'python-pycparser'
    'python-pyyaml'
    'python-ruamel-yaml'
    'python-toml'
    'python-tomli'
    'python-tomli-w'
    'python-click-default-group'
    'python-click-completion'
    'python-click-log'
    'python-colorlog'
    'python-loguru'
    'python-structlog'
    'python-json-logging'
    'python-ecs-logging'
    'python-sentry-sdk'
    'python-prometheus-client'
    'python-prometheus-fastapi-instrumentator'
    'python-fastapi'
    'python-uvicorn'
    'python-gunicorn'
    'python-uvloop'
    'python-httptools'
    'python-websockets'
    'python-redis'
    'python-hiredis'
    'python-celery'
    'python-kombu'
    'python-billiard'
    'python-vine'
    'python-amqp'
    'python-pika'
    'python-sqlalchemy'
    'python-psycopg2'
    'python-pymysql'
    'python-aiomysql'
    'python-asyncpg'
    'python-alembic'
    'python-sqlalchemy-utils'
    'python-marshmallow'
    'python-marshmallow-sqlalchemy'
    'python-sqlalchemy'
    'python-alembic'
    'python-pytest-asyncio'
    'python-aiosqlite'
    'python-pytest-benchmark'
    'python-pytest-cov'
    'python-pytest-html'
    'python-pytest-xdist'
    'python-pytest-timeout'
    'python-pytest-ordering'
    'python-pytest-lazy-fixture'
    'python-faker'
    'python-freezegun'
    'python-responses'
    'python-moto'
    'python-testfixtures'
    'python-pyfakefs'
    'python-nose'
    'python-pytest'
    'python-pytest-cov'
    'python-pytest-html'
    'python-pytest-xdist'
    'python-pytest-timeout'
    'python-pytest-ordering'
    'python-pytest-lazy-fixture'
    'python-pytest-benchmark'
    'python-pytest-asyncio'
    'python-pytest-mock'
    'python-pytest-runner'
)
makedepends=('python-setuptools' 'python-build' 'python-installer')
optdepends=(
    'nmap: Network scanning'
    'openvas: Vulnerability scanning'
    'nessus: Vulnerability scanning'
    'nikto: Web vulnerability scanning'
    'sqlmap: SQL injection scanning'
    'metasploit: Exploitation framework'
    'burpsuite: Web application security testing'
    'wireshark: Network protocol analyzer'
    'tcpdump: Network packet analyzer'
    'netcat: Network debugging'
)
options=(!emptydirs)
backup=('etc/safex/config.yaml')
install='safex.install'
changelog='CHANGELOG.md'

prepare() {
    cd "$srcdir/$pkgname-$pkgver"

    # Create Python virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install build dependencies
    pip install --upgrade pip setuptools wheel
}

build() {
    cd "$srcdir/$pkgname-$pkgver"
    source venv/bin/activate

    # Install project dependencies
    pip install -r requirements.txt

    # Build the package
    python -m build
}

check() {
    cd "$srcdir/$pkgname-$pkgver"
    source venv/bin/activate

    # Run tests
    pytest tests/ -v --cov=src --cov-report=html
}

package() {
    cd "$srcdir/$pkgname-$pkgver"

    # Install directories
    install -d "$pkgdir/opt/safex"
    install -d "$pkgdir/usr/bin"
    install -d "$pkgdir/etc/safex"
    install -d "$pkgdir/var/lib/safex/knowledge_base"
    install -d "$pkgdir/var/log/safex"
    install -d "$pkgdir/var/lib/safex/backups"
    install -d "$pkgdir/usr/share/licenses/safex"
    install -d "$pkgdir/usr/share/doc/safex"

    # Install source files
    cp -r src/* "$pkgdir/opt/safex/src/"
    cp -r configs/* "$pkgdir/etc/safex/"
    cp -r knowledge_base/* "$pkgdir/var/lib/safex/knowledge_base/"

    # Install scripts
    install -m755 scripts/*.sh "$pkgdir/opt/safex/scripts/"

    # Install main executable
    install -m755 safex.py "$pkgdir/opt/safex/safex.py"

    # Create symlink in /usr/bin
    ln -s /opt/safex/safex.py "$pkgdir/usr/bin/safex"

    # Install documentation
    install -m644 README.md "$pkgdir/usr/share/doc/safex/"
    install -m644 SECURITY.md "$pkgdir/usr/share/doc/safex/"
    install -m644 SAFE_TESTING.md "$pkgdir/usr/share/doc/safex/"
    install -m644 README_I18N.md "$pkgdir/usr/share/doc/safex/"
    install -m644 PROJECT_STRUCTURE.md "$pkgdir/usr/share/doc/safex/"
    install -m644 LICENSE "$pkgdir/usr/share/licenses/safex/" 2>/dev/null || echo "No LICENSE file found"

    # Install systemd service files (if they exist)
    if [ -f "safex.service" ]; then
        install -m644 safex.service "$pkgdir/usr/lib/systemd/system/"
    fi
}

post_install() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           SAFEX installed successfully!                    ║"
    echo "║                                                          ║"
    echo "║   Security Audit Framework for Enhanced Protection        ║"
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
    echo "   $ safex scan <target>"
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

    # Create log directory with proper permissions
    if [ ! -d "/var/log/safex" ]; then
        mkdir -p /var/log/safex
        chmod 755 /var/log/safex
    fi

    # Create backup directory
    if [ ! -d "/var/lib/safex/backups" ]; then
        mkdir -p /var/lib/safex/backups
        chmod 755 /var/lib/safex/backups
    fi

    echo "✅ Setup complete!"
    echo ""
}

pre_upgrade() {
    echo "🔄 Upgrading SAFEX..."
    echo ""
}

post_upgrade() {
    echo "✅ SAFEX upgraded successfully!"
    echo ""
    echo "📝 Check /usr/share/doc/safex/ for changelog"
    echo ""
}

pre_remove() {
    echo "⏳ Stopping SAFEX services..."
    systemctl stop safex 2>/dev/null || true
    systemctl disable safex 2>/dev/null || true
    echo "✅ Services stopped"
    echo ""
}

post_remove() {
    echo "🗑️  SAFEX removed"
    echo ""
    echo "⚠️  Configuration and data preserved:"
    echo "   - /etc/safex"
    echo "   - /var/lib/safex"
    echo "   - /var/log/safex"
    echo ""
    echo "To completely remove all data, run:"
    echo "   sudo rm -rf /etc/safex /var/lib/safex /var/log/safex"
    echo ""
}

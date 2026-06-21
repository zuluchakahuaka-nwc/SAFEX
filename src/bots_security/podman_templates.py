"""
Podman Templates - generates secure container deployment configurations
for Telegram bots (and other messaging platform bots).

All templates use PODMAN (not Docker). Includes:
- Secure Dockerfile (non-root, minimal)
- podman-compose.yml
- nginx reverse proxy config
- Systemd service unit (optional)
"""

from typing import Dict, Optional
from ..config.settings import Settings
from ..utils.logger import get_logger
from .models import PlatformType

logger = get_logger(__name__)


class PodmanTemplates:
    """Generates secure Podman deployment templates for bots."""

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or Settings()

    def generate_dockerfile(self, platform: PlatformType = PlatformType.TELEGRAM) -> str:
        return f'''FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash botuser

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential && \\
    pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt && \\
    apt-get purge -y build-essential && apt-get autoremove -y && \\
    rm -rf /var/lib/apt/lists/*

COPY . /app
RUN chown -R botuser:botuser /app

USER botuser

ENV PYTHONUNBUFFERED=1
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app:app"]
'''

    def generate_podman_compose(
        self,
        platform: PlatformType = PlatformType.TELEGRAM,
        domain: str = "bot.example.com",
    ) -> str:
        env_var = self._token_env_name(platform)
        return f'''# Podman Compose configuration for {platform.value} bot
# Usage: podman-compose up -d

version: "3.8"

services:
  bot:
    build:
      context: .
      dockerfile: Containerfile
    restart: unless-stopped
    environment:
      - {env_var}=${{{env_var}}}
      - WEBHOOK_SECRET=${{WEBHOOK_SECRET}}
    networks:
      - botnet
    expose:
      - "8000"
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: "0.5"
    tmpfs:
      - /tmp/uploads:rw,size=50m
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL

  nginx:
    image: docker.io/nginx:1.25-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    networks:
      - botnet
    depends_on:
      - bot

networks:
  botnet:
    driver: bridge
'''

    def generate_nginx_config(
        self, domain: str = "bot.example.com"
    ) -> str:
        return f'''user nginx;
worker_processes auto;

events {{ worker_connections 1024; }}

http {{
    limit_req_zone $binary_remote_addr zone=bot_req:10m rate=10r/m;

    server {{
        listen 443 ssl http2;
        server_name {domain};

        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;

        client_max_body_size 2M;
        limit_req zone=bot_req burst=20 nodelay;

        location /webhook {{
            proxy_pass http://bot:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 60s;
        }}

        location / {{
            return 404;
        }}
    }}

    server {{
        listen 80;
        server_name {domain};
        return 301 https://$host$request_uri;
    }}
}}
'''

    def generate_systemd_unit(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> str:
        return f'''[Unit]
Description={platform.value.capitalize()} Bot Service
After=network.target

[Service]
User=botuser
Group=botuser
WorkingDirectory=/srv/bot
EnvironmentFile=/etc/bot/secrets.env
ExecStart=/usr/bin/gunicorn -w 2 -b 127.0.0.1:8000 app:app
Restart=on-failure
RestartSec=10
ProtectSystem=full
ProtectHome=yes
PrivateTmp=yes
NoNewPrivileges=yes
ProtectKernelTunables=yes
ProtectControlGroups=yes

[Install]
WantedBy=multi-user.target
'''

    def generate_env_example(
        self, platform: PlatformType = PlatformType.TELEGRAM
    ) -> str:
        env_name = self._token_env_name(platform)
        return f'''# {platform.value.capitalize()} Bot Secrets
# NEVER commit this file to version control!
# Add to .gitignore

{env_name}=your_bot_token_here
WEBHOOK_SECRET=generate_a_long_random_string_here
'''

    def generate_all(
        self,
        platform: PlatformType = PlatformType.TELEGRAM,
        domain: str = "bot.example.com",
    ) -> Dict[str, str]:
        return {
            "Containerfile": self.generate_dockerfile(platform),
            "podman-compose.yml": self.generate_podman_compose(platform, domain),
            "nginx/nginx.conf": self.generate_nginx_config(domain),
            "systemd/bot.service": self.generate_systemd_unit(platform),
            ".env.example": self.generate_env_example(platform),
        }

    @staticmethod
    def _token_env_name(platform: PlatformType) -> str:
        mapping = {
            PlatformType.TELEGRAM: "TELEGRAM_TOKEN",
            PlatformType.DISCORD: "DISCORD_TOKEN",
            PlatformType.SLACK: "SLACK_TOKEN",
            PlatformType.VK: "VK_TOKEN",
            PlatformType.VIBER: "VIBER_TOKEN",
            PlatformType.WHATSAPP: "WHATSAPP_TOKEN",
            PlatformType.GENERIC: "BOT_TOKEN",
        }
        return mapping.get(platform, "BOT_TOKEN")

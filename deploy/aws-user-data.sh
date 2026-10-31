#!/bin/bash
set -euxo pipefail
exec > >(tee /var/log/lab5-setup.log | logger -t lab5-setup -s 2>/dev/console) 2>&1
dnf install -y docker git
systemctl enable --now docker
mkdir -p /usr/local/lib/docker/cli-plugins
curl -fSL https://github.com/docker/compose/releases/download/v5.6.0/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
curl -fSL https://github.com/docker/buildx/releases/download/v0.37.2/buildx-v0.37.2.linux-amd64 -o /usr/local/lib/docker/cli-plugins/docker-buildx
chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
git clone https://github.com/Miguel-ACD/el3302-lab5-pregunta1.git /opt/lab5-pregunta1
cd /opt/lab5-pregunta1
cat > .env <<EOF
APP_PORT=8000
POSTGRES_USER=lab5
POSTGRES_PASSWORD=$(openssl rand -hex 20)
POSTGRES_DB=champions
IMAGE_NAME=lab5-champions:aws
EOF
chmod 600 .env
docker compose up --build -d
docker compose ps

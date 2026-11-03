#!/bin/bash
set -e
cd "$(dirname "$0")"

git pull
docker compose -p nb4444spa -f docker/docker-compose-prod.yml up -d --build --remove-orphans
docker image prune -f

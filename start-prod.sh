#!/bin/bash
set -e
cd "$(dirname "$0")"

docker compose -p nb4444spa -f docker-compose-prod.yml up -d --build --remove-orphans
docker image prune -f

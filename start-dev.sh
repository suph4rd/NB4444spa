#!/bin/bash
set -e
cd "$(dirname "$0")"

docker-compose -p nb4444-dev -f docker-compose.yml up -d --build
docker image prune -f

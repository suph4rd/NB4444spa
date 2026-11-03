#!/bin/bash
set -e
cd "$(dirname "$0")/.."

docker compose -p nb4444-test -f docker-compose-test.yml up --build --remove-orphans
docker image prune -f

#!/bin/bash
set -e
cd "$(dirname "$0")/.."

git pull
docker-compose -f docker-compose-prod.yml up -d --build --remove-orphans
docker image prune -f

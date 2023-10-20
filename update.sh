#!/bin/bash                                                                     
git pull
docker-compose down --rmi local --remove-orphans
docker-compose -f docker-compose-prod.yml up -d --build

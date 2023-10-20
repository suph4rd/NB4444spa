#!/bin/bash
docker-compose -f docker-compose-test.yml down --rmi all
docker-compose -f docker-compose-test.yml up --build

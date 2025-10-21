#!/bin/bash

docker build --no-cache -f docker/Dockerfile_database -t counter_database:latest .

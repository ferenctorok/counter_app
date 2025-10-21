#!/bin/bash

echo "Building development docker image..."
docker build --no-cache -f ./docker/Dockerfile_app -t counter_app:latest .

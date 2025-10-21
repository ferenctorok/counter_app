#!/bin/bash

docker run \
    --name counter_database \
    -p 5432:5432 \
    -e POSTGRES_USER=appuser \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=appdb \
    --rm \
    -d \
    counter_database:latest

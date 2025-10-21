#!/bin/bash

docker run \
    --name counter_app \
    -e POSTGRES_USER=appuser \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=appdb \
    --network host \
    --mount type=bind,src=$(pwd),target=/home/dev_ws \
    --rm \
    -d \
    counter_app:latest \
    /bin/sh -c "cd /home/dev_ws && python3 -m pip install counter_app/ && fastapi run counter_app/main.py --port 80"

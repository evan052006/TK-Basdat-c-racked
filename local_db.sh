#!/bin/bash

# relaunch :)
docker rm db_tiktaktuk -f

docker run --name db_tiktaktuk \
        -e POSTGRES_PASSWORD=12345 \
        -e POSTGRES_DB=tiktaktuk \
        -p 5432:5432 \
        -d postgres

#!/bin/bash

export DOCKER_BUILDKIT=1

source .env

docker build -t power_grader_publish_server --build-arg GITHUB_AUTH_TOKEN=$GITHUB_AUTH_TOKEN --build-arg CACHEBUST=$(date +%s) .